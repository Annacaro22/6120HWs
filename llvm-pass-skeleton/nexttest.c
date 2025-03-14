/*
MIT License

Copyright (c) 2019 Barrett Otte

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


These combined files:
https://github.com/barrettotte/Linear-Algebra-C/blob/master/linear-algebra.h
https://github.com/barrettotte/Linear-Algebra-C/blob/master/vector.c
https://github.com/barrettotte/Linear-Algebra-C/blob/master/matrix.c
https://github.com/barrettotte/Linear-Algebra-C/blob/master/utils.h
https://github.com/barrettotte/Linear-Algebra-C/blob/master/utils.c


*/



#include <math.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

void assert(const int condition){
    if(!condition){
        printf("Assertion failed.\n");
        exit(1);
    }
}

bool exclusiveOr(bool a, bool b){
    return (a || b) && (!(a && b));
}

double roundn(double val, unsigned int n){
    assert(n > 0);
    double x = pow(10, n);
    return round(val * x) / x;
}

typedef struct{
    int rows; 
    int cols;
    double* data;
} matrix;

typedef struct{
    int cols;
    double* data;
} vector;


// Helper function for asserting matrix and matrix data
bool assertMatrix(matrix* m);


// Helper function for asserting vector and vector data
bool assertVector(vector* v);


// Return new matrix from double array d with size rows x cols
matrix* newMatrix(double* d, int rows, int cols);


// Return new vector from double array d with size cols
vector* newVector(double* d, int cols);


// Return new matrix with null data
matrix* nullMatrix(int rows, int cols);


// Return new vector with null data
vector* nullVector(int cols);


// Return new matrix as a zero matrix of size rows x cols
matrix* zeroMatrix(int rows, int cols);


// Return new vector as a zero vector of size cols
vector* zeroVector(int cols);


// Replace all elements in matrix m with n
void fillMatrix(matrix** m, double n);


// Replace all elements in vector v with n
void fillVector(vector** v, double n);


// Return new matrix as identifiy matrix of size n
matrix* identityMatrix(int n);


// Release matrix m from memory
void deleteMatrix(matrix* m);


// Release vector v from memory
void deleteVector(vector* v);


// Return new matrix as a copy of matrix m
matrix* copyMatrix(matrix* m);


// Return new vector as a copy of vector v
vector* copyVector(vector* v);


// Return matrix m as flattened vector
vector* flattenMatrix(matrix* m);


// Return number of elements of matrix m
int matrixSize(matrix* m);


// Return number of elements of vector v
int vectorSize(vector* v);


// Return size of matrix in bytes
int matrixSizeBytes(matrix* m);


// Return size of vector in bytes
int vectorSizeBytes(vector* v);


// Set element of matrix m[i,j] to scalar s
void setMatrixElement(matrix* m, int i, int j, double s);


// Return scalar as element m[i,j]
double getMatrixElement(matrix* m, int i, int j);


// Set element of vector v[i] to scalar s
void setVectorElement(vector* v, int i, double s);


// Return scalar as element v[i]
double getVectorElement(vector* v, int i);


// Set row vector i of matrix m to vector v
void setRowVector(matrix* m, int i, vector* v);


// Return new matrix as row vector i of vector v
vector* getRowVector(matrix* m, int i);


// Set col vector j of matrix m to vector v
void setColVector(matrix* m, int j, vector* v);


// Return new matrix as col vector j of vector v
vector* getColVector(matrix* m, int j);


// Return new vector as main diagonal of matrix m (square matrices only)
vector* getMainDiagonal(matrix* m);


// Set main diagonal of matrix m to vector v
void setMainDiagonal(matrix* m, vector* v);


// Return new vector as anti diagonal of matrix m (square matrices only)
vector* getAntiDiagonal(matrix* m);


// Set anti diagonal of matrix m to vector v
void setAntiDiagonal(matrix* m, vector* v);


// Return scalar as product of elements of main diagonal of matrix m
double diagonalProduct(matrix* m);


// "Pretty" print matrix m
void printMatrix(matrix* m, bool includeIndices);


// "Pretty" print vector v
void printVector(vector* v, bool includeIndices);


// Matrices m and n are equal if same dimension and identical elements
bool isMatrixEqual(matrix* m, matrix* n);


// Vectors v and w are equal if they contain identical elements
bool isVectorEqual(vector* v, vector* w);


// Matrices m and n have same dimensions if their columns and rows are equal
bool hasSameDimensions(matrix* m, matrix* n);


// Matrix m is a zero matrix if all elements are 0
bool isZeroMatrix(matrix* m);


// Matrix m is an identity matrix if it is a square matrix with only 1's along main diagonal
bool isIdentityMatrix(matrix* m);


// Matrix m is a square matrix if number of cols = number of rows
bool isSquareMatrix(matrix* m);


// Matrix m is invertible if it is a square matrix and det(m) != 0
bool isInvertible(matrix* m);


// Matrix m is a diagonal matrix if m is a square matrix and all elements not along diagonal are zero
bool isDiagonalMatrix(matrix* m);


// Matrix m is a triangular matrix if m is an upper triangular or lower triangular matrix
bool isTriangularMatrix(matrix* m);


// Matrix m is an upper triangular matrix if m is a square matrix and all elements below diagonal are zero
bool isUpTriMatrix(matrix* m);


// Matrix m is a lower triangular matrix if m is a square matrix and all elements above diagonal are zero
bool isLoTriMatrix(matrix* m);


// Matrix m is a symmetric matrix if m = transpose(m)
bool isMatrixSymmetric(matrix* m);


// Matrix m has a zero row if any row is made entirely of zeroes
bool hasZeroRow(matrix *m);


// Matrix m has a zero col if any col is made entirely of zeroes
bool hasZeroCol(matrix *m);


// Return new matrix as transpose of matrix m - flip matrix along diagonal
matrix* transposeMatrix(matrix* m);


// Return scalar as trace of matrix m - sum of all diagonals
double traceMatrix(matrix* m);


// Return new matrix as sum of matrices m1 and m2
matrix* addMatrices(matrix* m1, matrix* m2);


// Return new vector as sum of vectors v1 and v2
vector* addVectors(vector* v1, vector* v2);


// Return new matrix as matrix m ^ k
matrix* powMatrix(matrix* m, double k);


// Return new vector as vector v ^ k
vector* powVector(vector* v, double k);


// Return new matrix as product of matrices m1 and m2
matrix* multiplyMatrices(matrix* m1, matrix* m2);


// Return new matrix as matrix m scaled by scalar s
matrix* scaleMatrix(matrix* m, double s);


// Return scalar as dot product of vectors v1 and v2 (Euclidean inner product)
double dotProduct(vector* v, vector* w);


// Return new vector as cross product of vectors v1 and v2 (3 dimensions)
vector* crossProduct(vector* v, vector* w);


// Return scalar as vector magnitude of vector v (length or magnitude)
double vectorMagnitude(vector* v);


// Return scalar as euclidean distance between vectors v1 and v2
double vectorDistance(vector* v, vector* w);


// Return new vector as vector v scaled by s
vector* scaleVector(vector* v, double s);


// Vector v is a unit vector if the vectorMagnitude(v) = 1
bool isUnitVector(vector* v);


// Vector v1 is orthogonal (perpendicular) to vector v2 if dotProduct(v1, v2) == 0
bool isVectorOrthogonal(vector* v1, vector* v2);


// Matrix m1 is orthogonal to matrix m2 if inv(m) == transpose(m)
bool isMatrixOrthogonal(matrix* m1, matrix* m2);


// Return scalar of scalar triple product of vectors v1, v2, and v3
double scalarTripleProduct(vector* v1, vector* v2, vector* v3);


// Return new 2D matrix as reflection about x or y axis [x:0,y:1]
matrix* reflectAxis2D(matrix* m, int axis);


// Return new 3D matrix as reflection about xy,xz,yz plane [xy:0,xz:1,yz:2]
matrix* reflectAxis3D(matrix* m, int axis);


// Return new 2D matrix as orthogonal projection on x or y axis [x:0,y:1]
matrix* orthProj2D(matrix* m, int axis);


// Return new 3D matrix as orthogonal projection on xy,xz,yz plane [xy:0,xz:1,yz:2]
matrix* orthProj3D(matrix* m, int axis);


// Return new 2D matrix as rotation through angle theta
matrix* rotate2D(matrix *m, double theta);


// Return new nxn matrix as contraction or dilation of factor k on n-space
matrix* scaleNSpace(matrix *m, double k);


// Return new 2D matrix as shear of 2-space in x or y with factor k
matrix* shear2D(matrix *m, double k, int axis);


// Return scalar as determinant of matrix m
double determinant(matrix* m);


// Decompose matrix m into matrices l (lower triangular), u (upper triangular), p (permutation)
int luDecomposition(matrix* m, matrix** l, matrix** u, matrix** p);


// Return new matrix as submatrix of matrix m, excluding row i and col i
matrix* subMatrix(matrix* m, int i, int j);


// Return scalar as minor of matrix m at row i and column j
double elementMinor(matrix* m, int i, int j);


// Return new matrix as matrix of minors of matrix m
matrix* matrixMinor(matrix* m); 


// Return scalar as cofactor of matrix m at row i and column j
double elementCofactor(matrix* m, int i, int j);


// Return new matrix as cofactor matrix of matrix m
matrix* matrixCofactor(matrix* m);


// Return new matrix with elements alternating sign + -
matrix* signMatrix(int rows, int cols);


// Return new matrix as adjugate matrix of matrix m
matrix* adjugateMatrix(matrix* m);


// Return new matrix as inversion of matrix m
matrix* inverseMatrix(matrix* m);


// Return new matrix as pivot matrix of matrix m
matrix* pivotMatrix(matrix* m, int* swaps);










bool assertVector(vector* v){
    assert(v != NULL && v->data != NULL);
    return true;
}

vector* newVector(double* d, int cols){
    assert(d != NULL && cols > 0);
    vector* v = nullVector(cols);
    int idx = 0;
    for(int i = 0; i < v->cols; i++){
        v->data[i] = d[idx++];
    }
    return v;
}

vector* nullVector(int cols){
    assert(cols > 0);
    vector* v = (vector*) malloc(sizeof(vector));
    v->cols = cols;
    v->data = (double*) malloc(cols * sizeof(double));
    return v;
}

vector* zeroVector(int cols){
    vector* v = nullVector(cols);
    fillVector(&v, 0);
    return v;
}

void fillVector(vector** v, double n){
    assertVector(*v);
    for(int i = 0; i < (*v)->cols; i++){
        (*v)->data[i] = n;
    }
}

void deleteVector(vector* v){
    free(v->data);
    v->data = NULL;
    free(v);
    v = NULL;
}

vector* copyVector(vector* v){
    assertVector(v);
    vector* c = zeroVector(v->cols);
    for(int i = 0; i < v->cols; i++){
        c->data[i] = v->data[i];
    }
    return c;
}

int vectorSize(vector* v){
    assertVector(v);
    return v->cols;
}

int vectorSizeBytes(vector* v){
    return sizeof(double) * vectorSize(v);
}

bool isVectorEqual(vector* v, vector* w){
    assert(assertVector(v) && assertVector(w));
    if(v->cols != w->cols){
        return false;
    }
    for(int i = 0; i < v->cols; i++){
        if(v->data[i] != w->data[i]){
            return false;
        }
    }
    return true;
}

void setVectorElement(vector* v, int i, double s){
    assert(assertVector(v) && i >= 0 && i < v->cols);
    v->data[i] = s;
}

double getVectorElement(vector* v, int i){
    assert(assertVector(v) && i >= 0 && i < v->cols);
    return v->data[i];
}

void printVector(vector* v, bool includeIndices){
    assertVector(v);
    for(int i = 0; i < v->cols; i++){
        if(includeIndices){
            printf("[%d] -> ", i);
        }
        printf("%16.8f ", v->data[i]);
    }
}

double vectorMagnitude(vector* v){
    assertVector(v);
    double sum = 0;
    for(int i = 0; i < v->cols; i++){
        sum += (v->data[i] * v->data[i]);
    }
    return sqrt(sum);
}

bool isUnitVector(vector* v){
    return vectorMagnitude(v) == 1;
}

bool isVectorOrthogonal(vector* v1, vector* v2){
    assert(assertVector(v1) && assertVector(v2));
    return dotProduct(v1,v2) == 0;
}

double dotProduct(vector* v, vector* w){
    assert(assertVector(v) && assertVector(w) && v->cols == w->cols);
    double dp = 0;
    for(int i = 0; i < v->cols; i++){
        dp += (v->data[i] * w->data[i]);
    }
    return dp;
}

vector* crossProduct(vector* v, vector* w){
    assert(assertVector(v) && assertVector(w) && v->cols == 3 && v->cols == 3);
    vector* c = nullVector(3);
    c->data[0] = (v->data[1] * w->data[2]) - (v->data[2] * w->data[1]);
    c->data[1] = (v->data[0] * w->data[2]) - (v->data[2] * w->data[0]);
    c->data[2] = (v->data[0] * w->data[1]) - (v->data[1] * w->data[0]);
    return c;
}

double vectorDistance(vector* v, vector* w){
    assert(assertVector(v) && assertVector(w) && v->cols == w->cols);
    double d = 0;
    for(int i = 0; i < v->cols; i++){
        d += (w->data[i] - v->data[i]) * (w->data[i] - v->data[i]);
    }
    return sqrt(d);
}

vector* addVectors(vector* v, vector* w){
    assert(assertVector(v) && assertVector(w) && v->cols == w->cols);
    vector* sum = nullVector(v->cols);
    for(int i = 0; i < v->cols; i++){
        sum->data[i] = v->data[i] + w->data[i];
    }
    return sum;
}

vector* scaleVector(vector* v, double s){
    assert(assertVector(v));
    vector* scaled = nullVector(v->cols);
    for(int i = 0; i < v->cols; i++){
        scaled->data[i] = v->data[i] * s;
    }
    return scaled;
}

double scalarTripleProduct(vector* v1, vector* v2, vector* v3){
    assert(v1->cols == 3 && v2->cols == 3 && v3->cols == 3);
    return dotProduct(v1, crossProduct(v2, v3));
}

vector* powVector(vector* v, double k){
    assertVector(v);
    vector* p = nullVector(v->cols);
    for(int i = 0; i < v->cols; i++){
        p->data[i] = pow(v->data[i], k);
    }
    return p;
}





bool assertMatrix(matrix* m){
    assert(m != NULL && m->data != NULL);
    return true;
}

matrix* newMatrix(double* d, int rows, int cols){
    assert(d != NULL && rows > 0 && cols > 0);
    matrix* m = nullMatrix(rows, cols);
    int idx = 0;
    for(int i = 0; i < m->rows; i++){
        for(int j = 0; j < m->cols; j++){
            m->data[i * m->cols + j] = d[idx++];
        }
    }
    return m;
}

matrix* nullMatrix(int rows, int cols){
    assert(rows > 0 && cols > 0);
    matrix* m = (matrix*) malloc(sizeof(matrix));
    m->rows = rows;
    m->cols = cols;
    m->data = (double*) malloc(rows * cols * sizeof(double));
    return m;
}

matrix* zeroMatrix(int rows, int cols){
    matrix* m = nullMatrix(rows, cols);
    fillMatrix(&m, 0);
    return m;
}

void fillMatrix(matrix** m, double n){
    assertMatrix(*m);
    for(int i = 0; i < (*m)->rows; i++){
        for(int j = 0; j < (*m)->cols; j++){
            (*m)->data[i * (*m)->cols + j] = n;
        }
    }
}

matrix* identityMatrix(int n){
    matrix* m = zeroMatrix(n, n);
    for(int i = 0; i < m->rows; i++){
        for(int j = 0; j < m->rows; j++){
            if(i == j){
                m->data[i * m->cols + j] = 1;
            }
        }
    }
    return m;
}

void deleteMatrix(matrix* m){
    free(m->data);
    m->data = NULL;
    free(m);
    m = NULL;
}

matrix* copyMatrix(matrix* m){
    assertMatrix(m);
    matrix* c = zeroMatrix(m->rows, m->cols);
    for(int i = 0; i < m->rows; i++){
        for(int j = 0; j < m->cols; j++){
            c->data[i * m->cols + j] = m->data[i * m->cols + j];
        }
    }
    return c;
}

vector* flattenMatrix(matrix* m){
    assertMatrix(m);
    vector* flat = nullVector(m->rows * m->cols);
    int idx = 0;
    for(int i = 0; i < m->rows; i++){
        for(int j = 0; j < m->cols; j++){
            flat->data[idx++] = m->data[i * m->cols + j];
        }
    }
    return flat;
}

int matrixSize(matrix* m){
    assertMatrix(m);
    return m->rows * m->cols;
}

int matrixSizeBytes(matrix* m){
    return sizeof(double) * matrixSize(m);
}

void setMatrixElement(matrix* m, int i, int j, double s){
    assert(assertMatrix(m) && i >= 0 && j >= 0 && i < m->rows && j < m->cols);
    m->data[i * m->cols + j] = s;
}

double getMatrixElement(matrix* m, int i, int j){
    assert(assertMatrix(m) && i >= 0 && j >= 0 && i < m->rows && j < m->cols);
    return m->data[i * m->cols + j];
}

void setRowVector(matrix* m, int i, vector* v){
    assert(assertMatrix(m) && assertVector(v) && i >= 0 && i < m->rows);
    for(int j = 0; j < v->cols; j++){
        m->data[i * m->cols + j] = v->data[j];
    }
}

vector* getRowVector(matrix* m, int i){
    assert(assertMatrix(m) && i >= 0 && i < m->rows);
    double* row = (double*) malloc(sizeof(double) * m->cols);
    for(int j = 0; j < m->cols; j++){
        row[j] = m->data[i * m->cols + j];
    }
    vector* v = newVector(row, m->cols);
    free(row);
    return v;
}

void setColVector(matrix* m, int j, vector* v){
    assert(assertMatrix(m) && assertVector(v) && j >= 0 && j < m->cols);
    for(int i = 0; i < v->cols; i++){
        m->data[i * m->cols + j] = v->data[i];
    }
}

vector* getColVector(matrix* m, int j){
    assert(assertMatrix(m) && j >= 0 && j < m->cols);
    double* col = (double*) malloc(sizeof(double) * m->rows);
    for(int i = 0; i < m->rows; i++){
        col[i] = m->data[i * m->cols + j];
    }
    vector* v = newVector(col, m->rows);
    free(col);
    return v;
}

vector* getMainDiagonal(matrix* m){
    assert(isSquareMatrix(m));
    double* diag = (double*) malloc(sizeof(double) * m->rows);
    for(int x = 0; x < m->rows; x++){
        diag[x] = m->data[x * m->cols + x];
    }
    vector* v = newVector(diag, m->rows);
    free(diag);
    return v;
}

void setMainDiagonal(matrix* m, vector* v){
    assert(isSquareMatrix(m) && assertVector(v) && m->rows == m->cols && m->cols == v->cols);
    for(int x = 0; x < v->cols; x++){
        m->data[x * m->cols + x] = v->data[x];
    }
}

vector* getAntiDiagonal(matrix* m){
    assert(isSquareMatrix(m));
    int x = 0;
    double* diag = (double*) malloc(sizeof(double) * m->rows);
    for(int i = m->rows-1; i >= 0; i--){
        for(int j = m->cols-1; j >= 0; j--){
            if(i + j == m->rows-1){
                diag[x++] = m->data[i * m->cols + j];
                if(x == m->rows){
                    break;
                }
            }
        }
    }
    vector* v = newVector(diag, m->rows);
    free(diag);
    return v;
}

void setAntiDiagonal(matrix*m, vector* v){
    assert(isSquareMatrix(m) && assertVector(v) && m->rows == m->cols && m->cols == v->cols);
    int idx = 0;
    for(int i = m->rows-1; i >= 0; i--){
        for(int j = m->cols-1; j >= 0; j--){
            if(i + j == m->rows-1){
                m->data[i * m->cols + j] = v->data[idx++];
                if(idx == m->rows){
                    break;
                }
            }
        }
    }
}

double diagonalProduct(matrix*m){
    vector* diagonal = getMainDiagonal(m);
    double product = 1.0;
    for(int i = 0; i < diagonal->cols; i++){
        product *= diagonal->data[i];
    }
    deleteVector(diagonal);
    return product;
}

bool isMatrixEqual(matrix* m, matrix* n){
    assert(assertMatrix(m) && assertMatrix(n));
    if(m->rows != n->rows || m->cols != n->cols){
        return false;
    }
    for(int i = 0; i < m->rows; i++){
        for(int j = 0; j < m->cols; j++){
            if(m->data[i * m->cols + j] != n->data[i * n->cols + j]){
                return false;
            }
        }
    }
    return true;
}

bool hasSameDimensions(matrix* m, matrix* n){
    assert(assertMatrix(m) && assertMatrix(n));
    return (m->rows == n->rows) && (m->cols == n->cols);
}

bool isZeroMatrix(matrix* m){
    assertMatrix(m);
    for(int i = 0; i < m->rows; i++){
        for(int j = 0; j < m->cols; j++){
            if(m->data[i * m->cols + j] != 0){
                return false;
            }
        }
    }
    return true;
}

bool isIdentityMatrix(matrix* m){
    if(!isSquareMatrix(m)){
        return false;
    }
    for(int i = 0; i < m->rows; i++){
        for(int j = 0; j < m->cols; j++){
            if(i == j && m->data[i * m->cols + j] != 1.0){
                return false;
            } else if(i != j && m->data[i * m->cols + j] != 0.0) {
                return false;
            }
        }
    }
    return true;
}

bool isSquareMatrix(matrix* m){
    assertMatrix(m);
    return (m->rows == m->cols);
}

bool isInvertible(matrix* m){
    return isSquareMatrix(m) && determinant(m) != 0;
}

bool isDiagonalMatrix(matrix* m){
    assert(isSquareMatrix(m));
    for(int i = 0; i < m->rows; i++){
        for(int j = 0; j < m->cols; j++){
            if(i != j && m->data[i * m->cols + j] != 0){
                return false;
            }
        }
    }
    return true;
}

bool isTriangularMatrix(matrix* m){
    assert(isSquareMatrix(m));
    return exclusiveOr(isUpTriMatrix(m), isLoTriMatrix(m));
}

bool isUpTriMatrix(matrix* m){
    assert(isSquareMatrix(m));
    for(int i = 0; i < m->rows; i++){
        for(int j = 0; j < i; j++){
            if(m->data[i * m->cols + j] != 0){
                return false;
            }
        }
    }
    return true;
}

bool isLoTriMatrix(matrix* m){
    assert(isSquareMatrix(m));
    for(int i = 0; i < m->rows; i++){
        for(int j = i+1; j < m->cols; j++){
            if(m->data[i * m->cols + j] != 0){
                return false;
            }
        }
    }
    return true;
}

bool isMatrixSymmetric(matrix* m){
    matrix* t = transposeMatrix(m);
    bool equal = isMatrixEqual(m, t);
    deleteMatrix(t);
    return equal;
}

bool hasZeroRow(matrix* m){
    assertMatrix(m);
    bool allZeroes = true;
    for(int i = 0; i < m->rows; i++){
        for(int j = 0; j < m->cols; j++){
            if(m->data[i * m->cols + j] != 0){
                allZeroes = false;
            }
        }
        if(allZeroes){
            return true;
        }
        allZeroes = true;
    }
    return false;
}

bool hasZeroCol(matrix* m){
    assertMatrix(m);
    bool allZeroes = true;
    for(int j = 0; j < m->rows; j++){
        for(int i = 0; i < m->cols; i++){
            if(m->data[i * m->cols + j] != 0){
                allZeroes = false;
            }
        }
        if(allZeroes){
            return true;
        }
        allZeroes = true;
    }
    return false;
}

double determinant(matrix* m){
    assert(isSquareMatrix(m));
    switch(m->rows){  // use leibniz and laplace for smaller matrices
        case 1: return m->data[0];
        case 2: return (m->data[0] * m->data[3]) - (m->data[1] * m->data[2]);
        case 3: return (m->data[0]*((m->data[4]*m->data[8])-(m->data[5]*m->data[7]))) -
                       (m->data[1]*((m->data[3]*m->data[8])-(m->data[5]*m->data[6]))) +
                       (m->data[2]*((m->data[3]*m->data[7])-(m->data[4]*m->data[6]))) ;
    }
    if(isTriangularMatrix(m)){
        return diagonalProduct(m);
    }
    matrix* l = NULL;
    matrix* u = NULL;
    matrix* p = NULL;
    // det(permutation matrix) = (-1)^swaps
    double det = pow(-1, luDecomposition(m,&l,&u,&p)-1) * determinant(l) * determinant(u);
    deleteMatrix(p);
    deleteMatrix(u);
    deleteMatrix(l);
    return det;
}

matrix* transposeMatrix(matrix* m){
    assertMatrix(m);
    matrix* t = zeroMatrix(m->cols, m->rows);
    for(int i = 0; i < m->rows; i++){
        for(int j = 0; j < m->cols; j++){
            t->data[j * t->cols + i] = m->data[i * m->cols + j];
        }
    }
    return t;
}

double traceMatrix(matrix* m){
    assert(isSquareMatrix(m));
    double trace = 0;
    for(int i = 0; i < m->rows; i++){
        trace += m->data[i * m->cols + i];
    }
    return trace;
}

matrix* addMatrices(matrix* m, matrix* n){
    assert(hasSameDimensions(m, n));
    matrix* sum = nullMatrix(m->rows, m->cols);
    int idx = 0;
    for(int i = 0; i < m->rows; i++){
        for(int j = 0; j < m->cols; j++){
            sum->data[idx] = m->data[idx] + n->data[idx];
            idx++;
        }
    }
    return sum;
}

matrix* powMatrix(matrix* m, double k){
    assertMatrix(m);
    matrix* p = nullMatrix(m->rows, m->cols);
    for(int i = 0; i < m->rows; i++){
        for(int j = 0; j < m->cols; j++){
            p->data[i * m->cols + j] = pow(m->data[i * m->cols + j], k);
        }
    }
    return p;
}

matrix* multiplyMatrices(matrix* m, matrix* n){
    assert(assertMatrix(m) && assertMatrix(n) && m->cols == n->cols && m->rows == n->rows);
    matrix* prod = nullMatrix(m->rows, m->cols);
    for(int j = 0; j < m->rows; j++){
        for(int i = 0; i < m->cols; i++){
            double val = 0.0;
            for(int k = 0; k < m->cols; k++){
                val += ((m->data[i * m->cols + k] * n->data[k * m->cols + j]));
            }
            prod->data[i * m->cols + j] = val;
        }
    }
    return prod;
}

matrix* scaleMatrix(matrix* m, double s){
    assertMatrix(m);
    matrix* scaled = nullMatrix(m->rows, m->cols);
    for(int i = 0; i < m->rows; i++){
        for(int j = 0; j < m->cols; j++){
            scaled->data[i * m->cols + j] = m->data[i * m->cols + j] * s;
        }
    }
    return scaled;
}

matrix* subMatrix(matrix* m, int i, int j){
    assert(assertMatrix(m) && i >= 0 && i < m->rows && j >= 0 && j < m->cols);
    matrix* sm = nullMatrix(m->rows-1,m->cols-1);
    int idx = 0;
    for(int row = 0; row < m->rows; row++){
        for(int col = 0; col < m->cols; col++){
            if(row != i && col != j){
                sm->data[idx++] = m->data[row * m->cols + col];
            }
        }
    }
    return sm;
}

double elementMinor(matrix* m, int i, int j){
    matrix* sm = subMatrix(m,i,j);
    double minor = determinant(sm);
    deleteMatrix(sm);
    return minor;
}

matrix* matrixMinor(matrix* m){
    assertMatrix(m);
    matrix* mm = nullMatrix(m->rows, m->cols);
    for(int i = 0; i < mm->rows; i++){
        for(int j = 0; j < mm->cols; j++){
            mm->data[i * mm->cols + j] = elementMinor(m,i,j);
        }
    }
    return mm;
}

double elementCofactor(matrix* m, int i, int j){
    return pow(-1, (i+1)+(j+1)) * elementMinor(m, i, j);
}

matrix* matrixCofactor(matrix* m){
    assertMatrix(m);
    matrix* cfm = nullMatrix(m->rows, m->cols);
    for(int i = 0; i < cfm->rows; i++){
        for(int j = 0; j < cfm->cols; j++){
            cfm->data[i * cfm->cols + j] = elementCofactor(m,i,j);
        }
    }
    return cfm;
}

matrix* signMatrix(int rows, int cols){
    assert(rows > 0 && cols > 0);
    matrix* sm = nullMatrix(rows, cols);
    fillMatrix(&sm, 1);
    for(int i = 0; i < sm->rows; i++){
        for(int j = 0; j < sm->cols; j++){
            sm->data[i * sm->cols + j] = (((i * sm->cols + j)+1) % 2) ? 1 : -1;
        }
    }
    return sm;
}

matrix* adjugateMatrix(matrix* m){
    assertMatrix(m);
    matrix* mm = matrixMinor(m);
    matrix* sign = signMatrix(m->rows, m->cols);
    matrix* adj = multiplyMatrices(mm, sign);
    deleteMatrix(sign);
    deleteMatrix(mm);
    return adj;
}

int luDecomposition(matrix* m, matrix** l, matrix** u, matrix** p){
    assert(isSquareMatrix(m) && *l == NULL && *u == NULL && *p == NULL);
    int n = m->cols;
    int swaps = 0;
    *l = zeroMatrix(n, n);
    *u = zeroMatrix(n, n);
    *p = pivotMatrix(m, &swaps);
    matrix* m2 = multiplyMatrices(*p,m);
    for(int j = 0; j < n; j++){
        (*l)->data[j * n + j] = 1;
        for(int i = 0; i < j+1; i++){
            double sumU = 0;
            for(int k = 0; k < i; k++){
                sumU += ((*u)->data[k * n + j] * (*l)->data[i * n + k]);
            }
            (*u)->data[i * n + j] = m2->data[i * n + j] - sumU;
        }
        for(int i = j; i < n; i++){
            double sumL = 0;
            for(int k = 0; k < j; k++){
                sumL += ((*u)->data[k * n + j] * (*l)->data[i * n + k]);
            }
            (*l)->data[i * n + j] = (m2->data[i * n + j] - sumL) / (*u)->data[j * n + j];
        }
    }
    deleteMatrix(m2);
    return swaps;
}

matrix* inverseMatrix(matrix* m){
    assert(isInvertible(m));
    matrix* adj = adjugateMatrix(m);
    matrix* inv = scaleMatrix(adj,(1.0/determinant(m)));
    deleteMatrix(adj);
    return inv;
}

matrix* pivotMatrix(matrix* m, int* swaps){
    assert(isSquareMatrix(m));
    int n = m->cols;
    matrix* pivot = identityMatrix(n);
    for(int i = 0; i < n; i++){
        double max = m->data[i * n + i];
        int row = i;
        for(int j = i; j < n; j++){
            if(m->data[j * n + i] > max){
                max = m->data[j * n + i];
                row = j;
            }
        }
        if(i != row){
            vector* v = getRowVector(pivot, i);
            vector* w = getRowVector(pivot, row);
            setRowVector(pivot, i, w);
            setRowVector(pivot, row, v);
            deleteVector(w);
            deleteVector(v);
            swaps++;
        }
    }
    return pivot;
}

void printMatrix(matrix* m, bool includeIndices){
    assertMatrix(m);
    for(int i = 0; i < m->rows; i++){
        for(int j = 0; j < m->cols; j++){
            if(includeIndices){
                printf("[%d,%d] -> ", i, j);
            }
            printf("%8.2f ", m->data[i * m->cols + j]);
        }
        if(i < m->rows){
            printf("\n");
        }
    }
}

matrix* scaleNSpace(matrix* m, double k){
    assert(isSquareMatrix(m));
    matrix* n = zeroMatrix(m->cols,m->cols);
    vector* v = zeroVector(m->cols);
    fillVector(&v, k);
    setMainDiagonal(n, v);
    matrix* ref = multiplyMatrices(m, n);
    deleteVector(v);
    deleteMatrix(n);
    return ref;
}

matrix* reflectAxis2D(matrix* m, int axis){
    assert(isSquareMatrix(m) && m->cols == 2);
    matrix* n = zeroMatrix(2,2);
    setMatrixElement(n,0,0,(axis) ? 1 : -1);
    setMatrixElement(n,1,1,(axis) ? -1 : 1);
    matrix* ref = multiplyMatrices(m, n);
    deleteMatrix(n);
    return ref;
}

matrix* reflectAxis3D(matrix* m, int axis){
    assert(isSquareMatrix(m) && m->cols == 3 && axis >= 0 && axis <= 2);
    matrix* n = nullMatrix(3,3);
    if(axis == 0){
        double data[9] = {1,0,0,0,1,0,0,0,-1}; // XY
        setMainDiagonal(m, newVector(data, 3)); 
    } else if(axis == 1){
        double data[9] = {1,0,0,0,-1,0,0,0,1}; // XZ
        setMainDiagonal(m, newVector(data, 3)); 
    } else{
        double data[9] = {-1,0,0,0,1,0,0,0,1}; // YZ
        setMainDiagonal(m, newVector(data, 3)); 
    }
    matrix* ref = multiplyMatrices(m, n);
    deleteMatrix(n);
    return ref;
}

matrix* orthProj2D(matrix* m, int axis){
    assert(isSquareMatrix(m) && m->cols == 2);
    matrix* n = zeroMatrix(2,2);
    setMatrixElement(n,axis,axis,1);
    matrix* ref = multiplyMatrices(m,n);
    deleteMatrix(n);
    return ref;
}

matrix* orthProj3D(matrix* m, int axis){
    assert(isSquareMatrix(m) && m->cols == 3);
    matrix* n = zeroMatrix(3,3);
    switch(axis){
        case 0: // XY plane
            setMatrixElement(n,0,0,1);
            setMatrixElement(n,1,1,1); 
            break;
        case 1: // XZ plane
            setMatrixElement(n,0,0,1); 
            setMatrixElement(n,2,2,1);
            break;
        case 2: // YZ plane
            setMatrixElement(n,1,1,1);
            setMatrixElement(n,2,2,1);
            break;
    }
    matrix* ref = multiplyMatrices(m, n);
    deleteMatrix(n);
    return ref;
}

matrix* shear2D(matrix* m, double k, int axis){
    assert(isSquareMatrix(m) && m->cols == 2);
    matrix* n = zeroMatrix(2,2);
    setMatrixElement(n,0,0,1);
    setMatrixElement(n,0,1,(axis) ? k : 0);
    setMatrixElement(n,1,0,(axis) ? 0 : k);
    setMatrixElement(n,1,1,1);
    matrix* sheared = multiplyMatrices(m,n);
    deleteMatrix(n);
    return sheared;
}

matrix* rotate3D(matrix* m, double theta, int axis){
    assert(isSquareMatrix(m) && m->cols == 3);
    matrix* n = zeroMatrix(3,3);
    switch(axis){
        case 0: // X
            setMatrixElement(n,0,0,1);
            setMatrixElement(n,1,0,cos(theta));
            setMatrixElement(n,1,1,-sin(theta));
            setMatrixElement(n,2,1,sin(theta));
            setMatrixElement(n,2,2,cos(theta));
            break;
        case 1: // Y
            setMatrixElement(n,0,0,cos(theta));
            setMatrixElement(n,1,2,sin(theta));
            setMatrixElement(n,1,1,1);
            setMatrixElement(n,2,0,-sin(theta));
            setMatrixElement(n,2,2,cos(theta));
            break;
        case 2: // Z
            setMatrixElement(n,0,0,cos(theta));
            setMatrixElement(n,0,1,-sin(theta));
            setMatrixElement(n,2,0,sin(theta));
            setMatrixElement(n,2,1,cos(theta));
            setMatrixElement(n,2,2,1);
            break;
    }
    matrix* ref = multiplyMatrices(m, n);
    deleteMatrix(n);
    return ref;
}

int main() {
    return 0;
}