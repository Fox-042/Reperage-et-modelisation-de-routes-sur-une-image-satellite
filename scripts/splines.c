#include <stdio.h>
#include <stdlib.h>
#include <math.h>

typedef struct point{
    double x;
    double y;
} point;

typedef struct coord{
    int i;
    int j;
} coord;

typedef struct spline{
    double a;
    double b;
    double c; 
    double d;
} spline;

typedef struct fonction{
    int taille;
    spline** splines;
} fonction;

void splines_cubiques(fonction* sortie, double* x, double* y, int n){
    double* intervalles = malloc((n-1)*sizeof(double));
    for (int i=0; i<n-1;i++){
        intervalles[i]=x[i+1]-x[i];
    }
    double* alpha = malloc((n-1)* sizeof(double));
    alpha[0]=0;
    for (int i=1;i<n-1;i++){
        alpha[i]=(3.0/intervalles[i])*(y[i+1]-y[i])-(3.0/intervalles[i-1])*(y[i]-y[i-1]);
    }
    double* l = malloc((n)* sizeof(double));
    double* mu = malloc((n-1)* sizeof(double));
    double* z = malloc((n)* sizeof(double));
    l[0] = 1;
    mu[0] = 0;
    z[0] = 0;
    for (int i=1;i<n-1;i++){
        l[i]= 2*(x[i+1]-x[i-1])-intervalles[i-1]*mu[i-1];
        mu[i]= intervalles[i]/l[i];
        z[i] = (alpha[i]-intervalles[i-1]*z[i-1])/l[i];
    }
    l[n-1]=1;
    z[n-1]=0;
    
    double* a = y; //renommage pour lisiblilité; N'EST PAS UNE COPIE
    double* b = malloc(n*sizeof(double));
    double* c = malloc(n*sizeof(double));
    double* d = malloc(n*sizeof(double));

    c[n-1]=0;

    for(int i = n-2; i>-1;i--){
        c[i]=z[i]-mu[i]*c[i+1];
        b[i] = (y[i+1] - y[i])/intervalles[i] - intervalles[i]*(c[i+1] + 2*c[i]) / 3;
        d[i] = (c[i+1] - c[i]) / (3*intervalles[i]);
        sortie->splines[i]->a = a[i];
        sortie->splines[i]->b = b[i];
        sortie->splines[i]->c = c[i];
        sortie->splines[i]->d = d[i];
    }

    free(alpha);
    free(l);
    free(mu);
    free(z);
    free(b);
    free(c);
    free(d);
}

double evalue_spline(spline* s, double xi, double x){
    return s->a+ s->b*(x - xi) + s->c*(x - xi)*(x - xi) + s->d*(x - xi)*(x - xi)*(x - xi);
}

void permute(point ** tab, int i, int j){
    point* temp = tab[i];
    tab[i]=tab[j];
    tab[j]= temp;
}

void sort(point** tab,int n){
    for (int i=0;i<n;i++){
        double mini = tab[i]->x;
        int im = i;
        for(int j = i; j<n; j++){
            if (tab[j]->x<mini){
                permute(tab,j,im);
                im=j;
                mini=tab[j]->x;
            }
        }
    }
}

point * interpole(point** points,int n,int N, double deb, double fin){
    sort(points,n);
    double* X=malloc(n*sizeof(double));
    double* Y=malloc(n*sizeof (double));
    for(int i = 0;i<n;i++){
        X[i]=points[i]->x;
        Y[i]=points[i]->y;
    }
    double h = (fin-deb)/(N-1);
    point* courbe =malloc(N*sizeof (point));
    fonction * sp = malloc(sizeof(fonction));
    sp->taille = n-1;
    sp->splines=malloc((n-1)*sizeof(spline*));
    for (int i = 0; i < n-1; i++) {
        sp->splines[i] = malloc(sizeof(spline));
    }
    splines_cubiques(sp,X,Y,n);

    
    for(int i=0; i<N;i++){
        double x = deb+i*h;
        int j=0;
        while(j<n-2 && X[j+1]<=x){
            j++;
        }
        double a = sp->splines[j]->a;
        double b = sp->splines[j]->b;
        double c = sp->splines[j]->c;
        double d = sp->splines[j]->d;
        courbe[i].x = x;
        courbe[i].y = evalue_spline(sp->splines[j],X[j],x);

    }
  
     for (int i = 0; i < n-1; i++) {
        free(sp->splines[i]);
    }
    free(sp->splines);
    free(sp);
    free(X);
    free(Y);
    return courbe;
}

point** splines_paramatrees(point** points, int n, int N){

    point** pts_x=malloc(n*sizeof(point*));
    point** pts_y=malloc(n*sizeof (point*));

    double t_0 = 0;
    for(int i=0;i<n;i++){
        pts_x[i] = malloc(sizeof(point));
        pts_y[i] = malloc(sizeof(point));
        double t = t_0 + sqrt(points[i]->x*points[i]->x + points[i]->y* points[i]->y);
        t_0=t;
        pts_x[i]->x=t;
        pts_x[i]->y=points[i]->x;

        pts_y[i]->x=t;
        pts_y[i]->y=points[i]->y;
    }

    point* courbe_x = interpole(pts_x,n,N,pts_x[0]->x,pts_x[n-1]->x);
    point* courbe_y = interpole(pts_y,n,N,pts_y[0]->x,pts_y[n-1]->x);

    point** courbe_resultante = malloc((N)*sizeof(point*));

    for (int i= 0; i<N; i++){
        courbe_resultante[i] = malloc(sizeof(point));
        courbe_resultante[i]->x = courbe_x[i].y;
        courbe_resultante[i]->y = courbe_y[i].y;
    }
    for(int i = 0; i < n; i++) {
        free(pts_x[i]);
        free(pts_y[i]);
    }
    free(pts_x);
    free(pts_y);
    free(courbe_x);
    free(courbe_y);
    return courbe_resultante;
}


void lit_donnees(point*** points, int*n, int*N, char* nom_fichier){
    /*format du fichier donné en entrée:
    n
    N
    x,y
    ...
    */
    FILE* entree;
    
    entree = fopen(nom_fichier,"r");

    if (!entree) {
        perror("erreur fopen");
        return;
    }

    fscanf(entree,"%d\n",n);
    fscanf(entree,"%d\n",N);

    *points = malloc(*n*(sizeof(point*)));

    for (int i=0;i<*n;i++){
        (*points)[i] = malloc(sizeof(point));
        fscanf(entree,"%lf,%lf\n",&((*points)[i]->x),&((*points)[i]->y));
    }

    fclose(entree);
}

void ecrit_resultat(point** points, int n, int N, char* nom_fichier){
    /*format du fichier sortant:
    x,y
    ...

    La fonction ecrit le resultat final ET libere les points: fonction de "conclusion"
    */
    FILE* sortie;
    
    sortie = fopen(nom_fichier,"w+");

    if (!sortie) {
        perror("erreur fopen");
        return;
    }

    for (int i=0;i<N;i++){
        fprintf(sortie,"%lf,%lf\n",((points)[i]->x),(points)[i]->y);
        free(points[i]);
    }

    fclose(sortie);
    free(points);
}

int main(){
    int n;
    int N;
    point** points;
    lit_donnees(&points, &n, &N, "textes/entree.txt");
    point** resultat = splines_paramatrees(points, n, N);
    ecrit_resultat(resultat, n, N,"textes/sortie.txt");

    return 0;
}