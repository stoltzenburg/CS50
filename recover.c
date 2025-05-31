#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int BLOCK = 512;

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover FILE\n");
        return 1;
    }

    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    uint8_t buffer[BLOCK];
    FILE *img;
    char *filename = malloc(8);
    int num = 0;
    int found = 0;

    while (fread(buffer, 1, BLOCK, input) == 512)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff &&
            (buffer[3] & 0xf0) == 0xe0)
        {
            found = 1;
            if (num == 0)
            {
                img = fopen("000.jpg", "w");
                fwrite(buffer, 1, BLOCK, img);
            }
            else
            {
                fclose(img);
                sprintf(filename, "%03i.jpg", num);
                img = fopen(filename, "w");
                fwrite(buffer, 1, BLOCK, img);
            }
            num++;
        }
        else
        {
            if (found == 1)
            {
                fwrite(buffer, 1, BLOCK, img);
            }
        }
    }

    fclose(img);
    free(filename);
    fclose(input);
}
