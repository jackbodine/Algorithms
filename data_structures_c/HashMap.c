#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct HashMapEntry {
    char *key;  /* public */
    int value;  /* public */
    struct HashMapEntry *__prev;
    struct HashMapEntry *__next;
};

struct HashMapIter {
    int __bucket;
    struct HashMap *__map;
    struct HashMapEntry *__current;

    struct HashMapEntry* (*next)(struct HashMapIter* self);
    void (*del)(struct HashMapIter* self);
};

struct HashMap {
    /* Attributes */
    int __buckets;
    struct HashMapEntry *__heads[8];
    struct HashMapEntry *__tails[8];
    int __count;

    /* Methods */
    void (*put)(struct HashMap* self, char *key, int value);
    int (*get)(struct HashMap* self, char *key, int def);
    int (*size)(struct HashMap* self);
    void (*dump)(struct HashMap* self);
    struct HashMapIter* (*iter)(struct HashMap* self);
    void (*del)(struct HashMap* self);
};

void __HashMap_del(struct HashMap* self)
{
    int i;
    struct HashMapEntry *cur, *next;

    for(i=0; i<self->__buckets; i++) {
        cur = self->__heads[i];
        while(cur) {
            free(cur->key);
            /* value is just part of the struct */
            next = cur->__next;
            free(cur);
            cur = next;
        }
    }
    free((void *)self);
}

void __HashMapIter_del(struct HashMapIter* self) {
    free((void *)self);
}

int getBucket(char *str, int buckets)
{
    int hash = 42;
    if ( str == NULL ) return 0;
    for( ; *str ; str++) {
        hash = ( hash << 3 ) ^ *str;
    }
    return hash % buckets;
}

void __HashMap_dump(struct HashMap* self)
{
    int i;
    struct HashMapEntry *cur;
    printf("Object HashHashMap count=%d buckets=%d\n", self->__count, self->__buckets);
    for(i = 0; i < self->__buckets; i++ ) {
        for(cur = self->__heads[i]; cur != NULL ; cur = cur->__next ) {
            printf(" %s=%d [%d]\n", cur->key, cur->value, i);
        }
    }
}

/* Begin my code */

struct HashMapEntry* __HashMap_find(struct HashMap* self, char *key, int bucket)
{
    struct HashMapEntry *target;

    target = self->__heads[bucket];
    while (target != NULL) {
        if (strcmp(target->key, key) == 0) {
            return target;
        }
        target = target->__next;
    }

    return NULL;
}

void __HashMap_put(struct HashMap* self, char *key, int value) {
    int bucket;
    struct HashMapEntry *old, *new;
    char *new_key;

    if (key == NULL) return;

    bucket = getBucket(key, self->__buckets);
    old = __HashMap_find(self, key, bucket);

    // Replace if key already exists
    if (old != NULL) {
        old->value = value;
        return;
    }

    new = malloc(sizeof(*new));
    new_key = strdup(key);
    if (new == NULL || new_key == NULL) {
        free(new);
        free(new_key);
        return;
    }

    new->key = new_key;
    new->value = value;
    new->__prev = self->__tails[bucket];
    new->__next = NULL;

    if (self->__tails[bucket] != NULL) {    // Add to occupied bucket
        self->__tails[bucket]->__next = new;
    } else {
        self->__heads[bucket] = new;        // Add to empty bucket
    }
    self->__tails[bucket] = new;

    self->__count++;
}

int __HashMap_get(struct HashMap* self, char *key, int def)
{
    int bucket;
    struct HashMapEntry *entry;

    if (key == NULL) {
        return def;
    }

    bucket = getBucket(key, self->__buckets);
    entry = __HashMap_find(self, key, bucket);

    if (entry != NULL) {
        return entry->value;
    }

    return def;
}

int __HashMap_size(struct HashMap* self)
{
    return self->__count;
}

struct HashMapEntry* __HashMapIter_next(struct HashMapIter* self)
{
    if (self->__current != NULL) {
        self->__current = self->__current->__next;
    }

    while (self->__current == NULL && self->__bucket < self->__map->__buckets) {
        self->__bucket++;
        if (self->__bucket < self->__map->__buckets) {
            self->__current = self->__map->__heads[self->__bucket];
        }
    }

    return self->__current;
}

/* End my code */

struct HashMapIter* __HashMap_iter(struct HashMap* map)
{
    struct HashMapIter *iter = malloc(sizeof(*iter));
    iter->__map = map;
    iter->__bucket = 0;
    iter->__current = map->__heads[iter->__bucket];
    iter->next = &__HashMapIter_next;
    iter->del = &__HashMapIter_del;
    return iter;
}

struct HashMap * HashMap_new() {
    struct HashMap *p = malloc(sizeof(*p));
    int i;

    p->__buckets = 8;
    for(i=0; i < p->__buckets; i++ ) {
        p->__heads[i] = NULL;
        p->__tails[i] = NULL;
    }

    p->__count = 0;

    p->put = &__HashMap_put;
    p->get = &__HashMap_get;
    p->size = &__HashMap_size;
    p->dump = &__HashMap_dump;
    p->iter = &__HashMap_iter;
    p->del = &__HashMap_del;
    return p;
}

int main(void)
{
    struct HashMap * map = HashMap_new();
    struct HashMapEntry *cur;
    struct HashMapIter *iter;

    setvbuf(stdout, NULL, _IONBF, 0);  /* Internal */

    printf("Testing HashMap\n");
    map->put(map, "z", 8);
    map->put(map, "z", 1);
    map->put(map, "y", 2);
    map->put(map, "b", 3);
    map->put(map, "a", 4);
    map->dump(map);

    printf("size=%d\n", map->size(map));

    printf("z=%d\n", map->get(map, "z", 42));
    printf("x=%d\n", map->get(map, "x", 42));

    printf("\nIterate\n");
    iter = map->iter(map);
    while(1) {
        cur = iter->next(iter);
        if ( cur == NULL ) break;
        printf(" %s=%d\n", cur->key, cur->value);
    }
    iter->del(iter);

    map->del(map);
}
