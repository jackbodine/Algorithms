use core::ptr::{self, NonNull};
use core::mem;
use core::alloc::{GlobalAlloc, Layout};

use super::Locked;

const MAX_ORDER: usize = 20; // e.g. up to 2^20 bytes

/// For simplicity, each free block is stored in a linked list.
struct ListNode {
    next: Option<&'static mut ListNode>,
    order: usize,
}

pub struct BuddyAllocator {
    // One free list per order from 0..=MAX_ORDER
    free_lists: [Option<&'static mut ListNode>; MAX_ORDER + 1],
    heap_start: usize,
    heap_size: usize,
}

impl BuddyAllocator {
    /// Create an empty buddy allocator
    pub const fn new() -> Self {
        const EMPTY: Option<&'static mut ListNode> = None;
        BuddyAllocator {
            free_lists: [EMPTY; MAX_ORDER + 1],
            heap_start: 0,
            heap_size: 0,
        }
    }

    /// Initialize the allocator with the given heap bounds.
    ///
    /// This function is unsafe because the caller must guarantee that the
    /// given heap is valid and unused. Must be called only once.
    pub unsafe fn init(&mut self, heap_start: usize, heap_size: usize) {
        self.heap_start = heap_start;
        self.heap_size = heap_size;

        // Find the largest order block that fits in heap_size.
        // For simplicity, assume the entire heap fits exactly into a 2^order block
        // or find the largest block <= heap_size. Real code would handle leftover too.
        let order = largest_order_that_fits(heap_size);

        // Create a single, large free block
        let block_ptr = heap_start as *mut ListNode;
        block_ptr.write(ListNode {
            next: None,
            order,
        });

        // Put it in the corresponding free list
        self.free_lists[order] = Some(&mut *block_ptr);
    }

    /// Allocate a block of at least `layout.size()` bytes.
    fn allocate(&mut self, layout: Layout) -> *mut u8 {
        let needed_size = layout.size().max(layout.align());
        let order = order_for_size(needed_size);

        // 1) Find a free block at >= 'order'
        let mut current_order = order;
        while current_order <= MAX_ORDER {
            if let Some(free_block) = self.free_lists[current_order].take() {
                // Found a block at 'current_order', now split until it matches 'order'
                return self.split_block(free_block, current_order, order);
            } else {
                current_order += 1;
            }
        }

        // If we get here, no block is available
        ptr::null_mut()
    }

    /// Splits a block from 'from_order' down to 'to_order'.
    /// Returns a pointer to a block of size 2^to_order.
    fn split_block(&mut self, mut block: &'static mut ListNode,
                   from_order: usize, to_order: usize) -> *mut u8
    {
        let mut current_order = from_order;
        let mut block_ptr = block as *mut ListNode as usize;
        while current_order > to_order {
            let half_size = 1 << (current_order - 1);
            let buddy_ptr = block_ptr + half_size;

            // One half is returned to the free list
            let buddy_block = buddy_ptr as *mut ListNode;
            unsafe {
                buddy_block.write(ListNode {
                    next: None,
                    order: current_order - 1,
                });
            }
            // Insert buddy into the free list
            let buddy_ref = unsafe { &mut *buddy_block };
            buddy_ref.next = self.free_lists[current_order - 1].take();
            self.free_lists[current_order - 1] = Some(buddy_ref);

            // The other half continues splitting
            block_ptr = block_ptr; // same address
            current_order -= 1;
        }
        // Return final block
        block.order = to_order;
        block_ptr as *mut u8
    }

    /// Deallocate a block with the given layout.
    fn deallocate(&mut self, ptr: *mut u8, layout: Layout) {
        if ptr.is_null() {
            return;
        }
        let size = layout.size().max(layout.align());
        let order = order_for_size(size);

        self.free_block(ptr, order);
    }

    /// Free logic with buddy coalescing.
    fn free_block(&mut self, ptr: *mut u8, mut order: usize) {
        let mut block_addr = ptr as usize;

        loop {
            let buddy_addr = block_addr ^ (1 << order);

            // Attempt to find the buddy in the free list
            if let Some(found) = self.try_remove_buddy_from_free_list(buddy_addr, order) {
                // If we found it, coalesce: the merged block has order+1
                block_addr = block_addr.min(buddy_addr);
                order += 1;
            } else {
                // The buddy is not free => just insert this block and stop
                let free_block = block_addr as *mut ListNode;
                unsafe {
                    free_block.write(ListNode {
                        next: None,
                        order,
                    });
                }
                let free_ref = unsafe { &mut *free_block };
                free_ref.next = self.free_lists[order].take();
                self.free_lists[order] = Some(free_ref);
                break;
            }

            // If we merged, keep going until we can't merge higher.
            if order > MAX_ORDER {
                break; // we can't merge beyond the largest order
            }
        }
    }

    /// Removes the buddy from the free list if present. Returns Some if found.
    fn try_remove_buddy_from_free_list(&mut self, buddy_addr: usize, order: usize)
        -> Option<&'static mut ListNode>
    {
        // Just walk with `current` and `prev` without reversing pointers:
        let mut current = self.free_lists[order];
        let mut prev: Option<&'static mut ListNode> = None;

        while let Some(node) = current {
            let node_addr = node as *mut ListNode as usize;
            if node_addr == buddy_addr {
                // remove it
                match prev {
                    None => self.free_lists[order] = node.next,
                    Some(p) => p.next = node.next,
                }
                node.next = None;
                return Some(node);
            }
            prev = current;
            current = node.next;
        }
        // Not found
        None
    }
}

/// Reverse a linked list of `ListNode`
fn reverse_list(mut head: Option<&'static mut ListNode>) -> Option<&'static mut ListNode> {
    let mut new_head: Option<&'static mut ListNode> = None;

    while let Some(mut node) = head {
        head = node.next.take();
        node.next = new_head.take();
        new_head = Some(node);
    }
    new_head
}

/// Returns the smallest power-of-2 order that can fit `size`.
fn order_for_size(size: usize) -> usize {
    let mut order = 0;
    let mut current_size = 1;
    while current_size < size {
        current_size <<= 1;
        order += 1;
    }
    order
}

/// Returns the largest order that fits within `size`. 
/// E.g. if size >= 2^20, return 20; if size >= 2^19, return 19, etc.
fn largest_order_that_fits(size: usize) -> usize {
    let mut order = 0;
    let mut current_size = 1;
    while current_size << 1 <= size && order < MAX_ORDER {
        current_size <<= 1;
        order += 1;
    }
    order
}

unsafe impl GlobalAlloc for Locked<BuddyAllocator> {
    unsafe fn alloc(&self, layout: Layout) -> *mut u8 {
        let mut allocator = self.lock();
        allocator.allocate(layout)
    }

    unsafe fn dealloc(&self, ptr: *mut u8, layout: Layout) {
        let mut allocator = self.lock();
        allocator.deallocate(ptr, layout);
    }
}
