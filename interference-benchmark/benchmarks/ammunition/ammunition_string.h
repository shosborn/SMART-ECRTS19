#ifndef AMMUNITION_STRING_H
#define AMMUNITION_STRING_H

typedef unsigned int size_x;
//typedef __SIZE_TYPE__ size_x;

/*
  Forward declaration of functions
*/

void *ammunition_memcpy( void *, const void *, size_x );
void *ammunition_memset( void *, int, size_x );
int ammunition_memcmp ( const void *mem1, const void *mem2, size_x size );
void *ammunition_memmove ( void *s1, const void *s2, size_x n );
int ammunition_strcmp ( const char *str1, const char *str2 );

#endif /* AMMUNITION_STRING_H */

