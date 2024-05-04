#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct lnode {
    char *text;
    struct lnode *next;
};

struct pylist {
  struct lnode *head;
  struct lnode *tail;
  int count;
};

/* Constructor - lst = list() */
struct pylist * pylist_new() {
    struct pylist *p = malloc(sizeof(*p));
    p->head = NULL;
    p->tail = NULL;
    p->count = 0;
    return p;
}

/* Destructor - del(lst) */
void pylist_del(struct pylist* self) {
    struct lnode *cur, *next;
    cur = self->head;
    while(cur) {
        free(cur->text);
        next = cur->next;
        free(cur);
        cur = next;
    }
    free((void *)self);
}

/* Begin My Code */

/* print(lst) */
void pylist_print(struct pylist* self)
{
    printf("[");
  
    struct lnode *target = self->head;
    while(target != NULL){
        printf("\'%s\'", target->text);
        if (target->next != NULL){
           printf(", "); 
        }
        target = target->next;
    }
    printf("]\n");
}

/* len(lst) */
int pylist_len(const struct pylist* self)
{
    return self->count;
}

/* lst.append("Hello world") */
void pylist_append(struct pylist* self, char *str) {
  /* Create the new node */
  struct lnode *new_node = malloc(sizeof(struct lnode));
  new_node->text = malloc(strlen(str) + 1);
  strcpy(new_node->text, str);
  new_node->next = NULL;
  
  /* Update list */
    if (self->head == NULL) {
        /* If the list is empty, set the new node as both head and tail */
        self->head = new_node;
        self->tail = new_node;
    } else {
        /* If the list is not empty, append the new node to the end */
        self->tail->next = new_node;
        self->tail = new_node;
    }
  self->count += 1;
}

/* lst.index("Hello world") - if not found -1 */
int pylist_index(struct pylist* self, char *str)
{
  	struct lnode *target = self->head;
  	int count = 0;
  	while (target != NULL){
	    if (strcmp(target->text, str) == 0) {
         	return count; 
            }
            count++;
            target = target->next;
        }
  	return -1;
}

/* End My Code */

int main(void)
{
    setvbuf(stdout, NULL, _IONBF, 0);  /* Internal */

    struct pylist * lst = pylist_new();
    pylist_append(lst, "Hello world");
    pylist_print(lst);
    pylist_append(lst, "Catch phrase");
    pylist_print(lst);
    pylist_append(lst, "Brian");
    pylist_print(lst);
    printf("Length = %d\n", pylist_len(lst));
    printf("Brian? %d\n", pylist_index(lst, "Brian"));
    printf("Bob? %d\n", pylist_index(lst, "Bob"));
    pylist_del(lst);
}
