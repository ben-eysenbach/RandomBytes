// Implements a Priority Queue ADT using a Binary Max Heap

#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <string.h>


// maximum number of elements in the heap
#define MAX_SIZE 256



// structs
struct Item {
    int key;
    char name[MAX_SIZE];
};

struct Heap {
    int size;
    struct Item array[MAX_SIZE];
};

// functions
int Heap_size(struct Heap *heap);
void Heap_swap(struct Heap *heap, int index1, int index2);
void Heap_down(struct Heap *heap, int index);
void Heap_up(struct Heap *heap, int index);
void Heap_print(struct Heap *heap);
void Heap_validate(struct Heap *heap);


// function definitions

void die(char *message)
{
    printf("ERROR: %s\n", message);
    exit(1);
}

void print_usage()
{
    printf("USAGE:\n");
    printf("\theap a[dd] <filename> <key> <name>\n");
    printf("\theap c[reate] <filename>\n");
    printf("\theap m[ax] <filename>\n");
    printf("\theap p[rint] <filename>\n");
    printf("\theap r[emove] <filename> <index>\n");
    printf("\theap u[update] <filename> <index> <new key>\n");
}

struct Heap *Heap_create()
{
    struct Heap *heap = malloc(sizeof(struct Heap));
    heap->size = 0;
    return heap;
}

void Heap_destroy(struct Heap *heap)
{
    if (heap) {
        // fflush(heap->file);
        // fclose(heap->file);
        free(heap);
    }
}

struct Heap *Heap_read(char *filename)
{
    struct Heap *heap = malloc(sizeof(struct Heap));
    if (!heap) {
        die("Memory error");
    }

    FILE *file = fopen(filename, "r+");
    int rc = fread(heap->array, sizeof(heap->array), 1, file);

    if (rc != 1) {
        die("Failed to load heap");
    }

    fflush(file);
    fclose(file);
    heap->size = Heap_size(heap);
    Heap_validate(heap);
    return heap;
}

void Heap_write(struct Heap *heap, char *filename)
{
    Heap_validate(heap);
    FILE *file = fopen(filename, "w");
    int rc = fwrite(heap->array, sizeof(heap->array), 1, file);
    if (rc != 1) {
        die("writing to file");
    }
    rc = fflush(file);
    if (rc == -1) {
        die("Cannot flush heap");
    }
    fclose(file);
}

void Heap_add(struct Heap *heap, int key, char *name)
{
    heap->size++;
    // binary heaps must be 1-indexed
    // The first element goes has index=1
    struct Item *item = &heap->array[heap->size];
    item->key = key;
    strncpy(item->name, name, MAX_SIZE);
    Heap_up(heap, heap->size);
}

void Heap_update(struct Heap *heap, int index, int key)
{
    int old_key = heap->array[index].key;
    heap->array[index].key = key;

    if (key > old_key) {

        Heap_up(heap, index);
    } else if (key < old_key) {

        Heap_down(heap, index);
    }
}

void Heap_remove(struct Heap *heap, int index)
{
    printf("Heap_remove(%d)\n", index);
    Heap_print(heap);

    int left_index = index * 2;
    int right_index = left_index + 1;
    struct Item *item = &heap->array[index];


    if (index > heap->size) {
        return;
    } else if (index == heap->size) {
        heap->array[index].key = '\0';
        heap->size--;
    } else if (left_index > heap->size) {
        // If removing an item which is a leaf but not the last leaf,
        // copy the last leaf over
        item->key = heap->array[heap->size].key;
        strncpy(item->name, heap->array[heap->size].name, MAX_SIZE);
        heap->array[heap->size].key = '\0';
        heap->size--;
        Heap_up(heap, index);
    } else if (right_index > heap->size) {
        item->key = heap->array[left_index].key;
        strncpy(item->name, heap->array[left_index].name, MAX_SIZE);
        heap->array[left_index].key = '\0';
        heap->size--;
    } else if (heap->array[left_index].key > heap->array[right_index].key) {
        item->key = heap->array[left_index].key;
        strncpy(item->name, heap->array[left_index].name, MAX_SIZE);
        heap->array[left_index].key = '\0';
        // heap->size--;
        Heap_remove(heap, left_index);
    } else { //heap->array[right_index].key > heap->array[left_index].key
        item->key = heap->array[right_index].key;
        strncpy(item->name, heap->array[right_index].name, MAX_SIZE);
        heap->array[right_index].key = '\0';
        // heap->size--;
        Heap_remove(heap, right_index);
    }
}

char *Heap_max(struct Heap *heap)
{
    return heap->array[0].name;
}

// heapify up
void Heap_up(struct Heap *heap, int index)
{
    int parent = index / 2;
    if (parent < 1) {
        return;
    }
    int parent_key = heap->array[parent].key;
    int key = heap->array[index].key;
    if (key > parent_key) {
        Heap_swap(heap, index, parent);
        Heap_up(heap, parent);
    }
}

// heapify down
void Heap_down(struct Heap *heap, int index)
{
    if (index > MAX_SIZE) {
        return;
    }
    int left_index = 2 * index;
    int right_index = left_index + 1;
    int key = heap->array[index].key;
    int left_key = heap->array[left_index].key;
    int right_key = heap->array[right_index].key;
    if (key > left_key && key > right_key) {
        return;
    } else if (left_key >= right_key) {
        Heap_swap(heap, index, left_index);
        Heap_down(heap, left_index);
    } else {
        Heap_swap(heap, index, right_index);
        Heap_down(heap, right_index);
    }
}
//
void Heap_swap(struct Heap *heap, int index1, int index2)
{
    assert(0 < index1 < MAX_SIZE);
    assert(0 < index2 < MAX_SIZE);
    struct Item *item1 = malloc(sizeof(struct Item));
    item1->key = heap->array[index1].key;
    strncpy(item1->name, heap->array[index1].name, MAX_SIZE);
    heap->array[index1] = heap->array[index2];
    heap->array[index2] = *item1;
}

void Heap_print(struct Heap *heap)
{

    printf("Size: %d\n", heap->size);
    printf("Elements: \n");
    for (int i = 1; i <= heap->size; i++) {
        printf("\tname: %s; key: %d\n",
                heap->array[i].name,
                heap->array[i].key);
    }
    printf("\n");
}

int Heap_size(struct Heap *heap)
{
    // Finds the number of non-null elements in an array
    // The first entry (with index 0) is NULL be default
    // so we can index starting at 1
    for (int i = 1; i < MAX_SIZE; i++) {
        if (heap->array[i].key == '\0') {
            return i-1;
        }
    }
    return 0;
}

void Heap_validate(struct Heap *heap)
{
    if (heap->size != Heap_size(heap)) {
        die("Incorrect size");
    }
    for (int index = 1; index < heap->size / 2; index++) {
        struct Item *parent = &heap->array[index];
        struct Item *left = &heap->array[2 * index];
        struct Item *right = &heap->array[2 * index + 1];
        if (parent->key == '\0') {
            die("Null key");
        }
        if (left->key > parent->key || right->key > parent->key) {
            die("Child greater than parent");
        }
    }
    // printf("Validate: passed\n");
}

int main(int argc, char *argv[])
{
    if (argc <= 2) {
        print_usage();
        die("Invalid arguments");
        return 1;
    }
    char *filename = argv[2];
    struct Heap *heap;
    int key;
    int index;
    char *name;
    char action = argv[1][0];
    printf("Action: %c\n", action);
    switch(action) {

        case 'a':
            heap = Heap_read(filename);
            key = atoi(argv[3]);
            name = argv[4];
            Heap_add(heap, key, name);
            Heap_write(heap, filename);
            break;

        case 'c':
            heap = Heap_create();
            Heap_write(heap, filename);
            break;

        case 'm':
            heap = Heap_read(filename);
            char *name = Heap_max(heap);
            printf("Max: %s\n", name);
            break;

        case 'p':
            heap = Heap_read(filename);
            Heap_print(heap);
            break;

        case 'r':
            heap = Heap_read(filename);
            index = atoi(argv[3]);
            Heap_remove(heap, index);
            break;

        case 'u':
            heap = Heap_read(filename);
            index = atoi(argv[3]);
            key = atoi(argv[4]);
            Heap_update(heap, index, key);
            Heap_write(heap, filename);
            break;

        default:
            print_usage();
            die("Invalid action");
            return 1;
    }

    Heap_destroy(heap);
    return 0;
}
