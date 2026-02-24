#include <stdio.h>

/** //
 * This is just a multiline comment.
 * //
 * This might come as a surprise.
*/
int main()
{
    int a = 0, b = 9;

    int y = 0;  // This is just a comment.

    ///* This is a multiline comment // */ a = 1;

    /* This is a multiline comment 2 */ a = 1; ///* Another comment in the line */ b = 8;


    printf("This is a: %d\nThis is b: %d\n", a, b); /**/

    char *temp = " This is just not what it used to be"
    "This is a temp string";

    printf("This is //  the char: %s", temp);

    return 0;
}