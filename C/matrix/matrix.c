#include <stdio.h>
#include <stdlib.h>

struct Matrix{
    int shape[2];
    int size;
    int **array;
};

struct Matrix *Matrix_zeros(int shape[2])
{
    int rows = shape[0];
    int cols = shape[1];
    struct Matrix *m = malloc(sizeof(struct Matrix));
    m->shape[0] = rows;
    m->shape[1] = cols;
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            m->array[i][j] = 1;
        }
    }
    return m;
}

struct Matrix *Matrix_random(int shape[2])
{
    int rows = shape[0];
    int cols = shape[1];
    struct Matrix *m = malloc(sizeof(struct Matrix));
    m->shape[0] = rows;
    m->shape[1] = cols;
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            m->array[i][j] = rand() % 10;
        }
    }
    return m;
}



void Matrix_print(struct Matrix *m)
{
    int rows = m->shape[0];
    int cols = m->shape[1];
    for (int i = 0; i < rows; i++) {
        printf("[");
        for (int j = 0; j < cols; j++) {
            printf("%3d,", m->array[i][j]);
        }
        printf("]\n");
    }
}


int main(int argc, char *argv[])
{
    int shape[] = {2, 4};
    struct Matrix *m = Matrix_random(shape);
    Matrix_print(m);
    return 0;
}
