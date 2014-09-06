#include <stdio.h>
#include <stdlib.h>

struct List
{
    struct Cell *first;
    struct Cell *last;
    int length;
};

struct Cell
{
    int value;
    struct Cell *prev;
    struct Cell *next;
};

struct List *List_create()
{
    struct List *list = malloc(sizeof(struct List));
    // list->length = 0;
    return list;
}

void List_append(struct List *list, int value)
{
    struct Cell *last = malloc(sizeof(struct Cell));
    last->value = value;
    if (list->length == 0) {
        list->first = last;
        list->last = last;
    } else {
        list->last->next = last;
        last->prev = list->last;
        list->last = last;
    }
    list->length++;
}

int List_pop(struct List *list)
{
    struct Cell *last = list->last;
    list->last = last->prev;
    list->length--;
    return last->value;
}

void List_print(struct List *list)
{
    printf("[");
    if (list->first) {
        struct Cell *cell = list->first;
        printf("%3d,", cell->value);
        while (cell->next) {
            printf("%3d,", cell->value);
            cell = cell->next;
        }
    }
    printf("]\n");
}


// struct List *List_reverse(struct List *list)
// {
//     struct List *reversed = malloc(sizeof(struct List));
//     if (list->length == 0) {
//         return reversed;
//     } else if (list->length == 1) {
//         reversed;
//     }
// }

int main(int argc, char *argv[])
{
    struct List *list = List_create();
    List_append(list, 1);
    List_append(list, 2);
    // List_append(list, 3);
    // printf("Length: %d\n", list->length);
    // printf("1: %d\n", list->first->value);
    List_print(list);

    return 0;
}
