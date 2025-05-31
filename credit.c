#include <cs50.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int validate(long long card, string card_str);
string card_type(long long card, string card_str);
int get_digit(long long card, int i);

int main(void)
{
    long long card = get_long("Number: ");
    char card_str[20];
    sprintf(card_str, "%lld", card);
    if (validate(card, card_str) == 1)
    {
        printf("%s\n", card_type(card, card_str));
    }
    else
    {
        printf("INVALID\n");
    }
}

int validate(long long card, string card_str)
{
    long digit_sum = 0;
    long multi_sum = 0;
    if (13 <= strlen(card_str) && strlen(card_str) <= 16)
    {
        // Luhn's Algo
        for (int i = 1; i <= strlen(card_str); i++)
        {
            if (i % 2 == 0)
            {
                int digit = get_digit(card, i) * 2;
                if (digit >= 10)
                {
                    // Split
                    multi_sum += digit % 10;
                    multi_sum += (digit - (digit % 10)) / 10;
                }
                else
                {
                    multi_sum += digit;
                }
            }
            else
            {
                digit_sum += get_digit(card, i);
            }
        }
        if ((digit_sum + multi_sum) % 10 == 0)
        {
            return true;
        }
        else
        {
            return false;
        }
    }
    else
    {
        return false;
    }
}

int get_digit(long long card, int i)
{
    // get int
    long power = pow(10, i);
    long power_less = pow(10, (i - 1));
    int digit = 0;
    if (power_less > 0)
    {
        digit = (((card % power) - (card % power_less)) / power_less);
    }
    else
    {
        digit = (card % power);
    }
    return digit;
}

string card_type(long long card, string card_str)
{
    // Card type
    if (strlen(card_str) == 15 && card_str[0] == '3' && (card_str[1] == '4' || card_str[1] == '7'))
    {
        return "AMEX";
    }
    else if (strlen(card_str) == 16 && card_str[0] == '5' && 1 <= (card_str[1] - '0') &&
             (card_str[1] - '0') <= 5)
    {
        return "MASTERCARD";
    }
    else if ((strlen(card_str) == 13 || strlen(card_str) == 16) && card_str[0] == '4')
    {
        return "VISA";
    }
    else
    {
        return "INVALID";
    }
}
