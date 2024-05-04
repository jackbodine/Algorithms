#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct dnode {
    char *key;
    char *value;
    struct dnode *next;
};

struct pydict {
  struct dnode *head;
  struct dnode *tail;
  int count;
};

/* Constructor - dct = dict() */
struct pydict * pydict_new() {
    struct pydict *p = malloc(sizeof(*p));
    p->head = NULL;
    p->tail = NULL;
    p->count = 0;
    return p;
}

/* Destructor - del(dct) */
void pydict_del(struct pydict* self) {
    struct dnode *cur, *next;
    cur = self->head;
    while(cur) {
        free(cur->key);
        free(cur->value);
        next = cur->next;
        free(cur);
        cur = next;
    }
    free((void *)self);
}

/* Begin my code */

/* print(dct) */
/* {'z': 'W', 'y': 'B', 'c': 'C', 'a': 'D'} */
void pydict_print(struct pydict* self)
{
    struct dnode *target = self->head;
    
    printf("{");
    
    while (target != NULL) {
        if (self->head != target) {
            printf(", ");
        }
        
        printf("'%s': '%s'", target->key, target->value);
        
        target = target->next;
    }
    
    printf("}\n");
}

int pydict_len(const struct pydict* self)
{
    return self->count;
}

/* find a node - used in get and put */
struct dnode* pydict_find(struct pydict* self, char *key)
{
    struct dnode *target = self->head;
    
    while (target != NULL) {
        if (strcmp(target->key, key) == 0) {
            return target;
        }
        target = target->next;
    }
    
    return NULL;
}

/* x.get(key) - Returns NULL if not found */
char* pydict_get(struct pydict* self, char *key)
{
    struct dnode *target = self->head;
    
    while (target != NULL) {
        if (strcmp(target->key, key) == 0) {
            return target->value;
        }
        target = target->next;
    }
    
    return NULL;
}

/* x[key] = value; Insert or replace the value associated with a key */
void pydict_put(struct pydict* self, char *key, char *value)
{
      struct dnode *target = self->head;
    
    // Search for existing key
    while (target != NULL) {
        if (strcmp(target->key, key) == 0) {
            // Key already exists, replace the value
            free(target->value);
            target->value = strdup(value);
            return;
        }
        target = target->next;
    }
    
    // Key not found, create a new node
    struct dnode *new_node = malloc(sizeof(struct dnode));
    new_node->key = strdup(key);
    new_node->value = strdup(value);
    new_node->next = NULL;
    
    // If the dictionary is empty, set the new node as head
    if (self->head == NULL) {
        self->head = new_node;
        self->tail = new_node;
    } else {
        // Append the new node to the end of the list
        self->tail->next = new_node;
        self->tail = new_node;
    }
    
    self->count++;
}

/* End my code */

int main(void)
{
    struct dnode * cur;
    struct pydict * dct = pydict_new();

    setvbuf(stdout, NULL, _IONBF, 0);  /* Internal */

    pydict_put(dct, "z", "Catch phrase");
    pydict_print(dct);
    pydict_put(dct, "z", "W");
    pydict_print(dct);
    pydict_put(dct, "y", "B");
    pydict_put(dct, "c", "C");
    pydict_put(dct, "a", "D");
    pydict_print(dct);
    printf("Length =%d\n",pydict_len(dct));

    printf("z=%s\n", pydict_get(dct, "z"));
    printf("x=%s\n", pydict_get(dct, "x"));

    printf("\nDump\n");
    for(cur = dct->head; cur != NULL ; cur = cur->next ) {
        printf("%s=%s\n", cur->key, cur->value);
    }

    pydict_del(dct);
}
