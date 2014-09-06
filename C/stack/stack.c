#include <stdio.h>
#include <stdlib.h>


// maximum size of the stack
#define MAX_SIZE 256

struct Stack {
    int array[MAX_SIZE];
    // index points to the last occupied entry. This is entry
    // which was added most recently. It should be the first
    // to be popped from the stack.
    int index;
};

void die(char *message)
{
    printf("ERROR: %s\n", message);
    exit(1);
}

struct Stack *Stack_create() {
    struct Stack *stack = malloc(sizeof(struct Stack));
    stack->index = -1;
    return stack;
}

void Stack_destroy(struct Stack *stack)
{
    free(stack);
}

struct Stack *Stack_read(char *filename)
{
    struct Stack *stack = Stack_create();
    FILE *file = fopen(filename, "r+");
    int rc = fread(stack, sizeof(struct Stack), 1, file);
    if (rc != 1) {
        die("Reading stack\n");
    }
    fflush(file);
    fclose(file);
    return stack;
}

void Stack_write(struct Stack *stack, char *filename)
{
    FILE *file = fopen(filename, "w");
    int rc = fwrite(stack, sizeof(struct Stack), 1, file);
    if (rc != 1) {
        die("writing stack\n");
    }
    fflush(file);
    fclose(file);
}

void Stack_push(struct Stack *stack, int num)
{
    stack->index++;
    if (stack->index > MAX_SIZE) {
        die("Stack overflow!\n");
    }
    stack->array[stack->index] = num;
}

int Stack_pop(struct Stack *stack)
{
    if (stack->index == -1) {
        die("Stack already empty");
    }
    int num = stack->array[stack->index];
    stack->index--;
    return num;
}

void Stack_print(struct Stack *stack)
{
    printf("Index: %d\n", stack->index);
    printf("Elements (oldest->newest):\n");
    for (int i = 0; i <= stack->index; i++) {
        printf("\t%d\n", stack->array[i]);
    }
    printf("\n");
}

int main(int argc, char *argv[])
{
    if (argc < 3) {
        die("USAGE: stack <filename> <action> [num]\n");
    }
    // using words instead of the first letter is also OK,
    // but I must use a char for "Switch"
    char action = argv[2][0];
    char *filename = argv[1];
    struct Stack *stack;
    int num;

    switch(action) {
        // create
        case 'c':
            stack = Stack_create();
            break;

        // push ("add")
        case 'a':
            num = atoi(argv[3]);
            stack = Stack_read(filename);
            Stack_push(stack, num);
            break;

        // pop ("remove")
        case 'r':
            stack = Stack_read(filename);
            num = Stack_pop(stack);
            printf("Popped: %d\n", num);
            break;

        // print
        case 'p':
            stack = Stack_read(filename);
            Stack_print(stack);
            break;

        default:
            die("USAGE: stack <filename> <action> [num]\n");
    }

    Stack_write(stack, filename);
    Stack_destroy(stack);

    return 0;
}
