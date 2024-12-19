#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    // Loop over all pixels
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Take average of red, green, and blue
            uint8_t average = round(
                (float) ((image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) /
                         3.0));

            // Update pixel values
            image[i][j].rgbtBlue = average;
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtRed = average;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    // Loop over all pixels
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            uint8_t tmpRed = image[i][j].rgbtRed;
            uint8_t tmpGreen = image[i][j].rgbtGreen;
            uint8_t tmpBlue = image[i][j].rgbtBlue;

            image[i][j].rgbtRed = image[i][width - 1 - j].rgbtRed;
            image[i][j].rgbtGreen = image[i][width - 1 - j].rgbtGreen;
            image[i][j].rgbtBlue = image[i][width - 1 - j].rgbtBlue;

            image[i][width - 1 - j].rgbtRed = tmpRed;
            image[i][width - 1 - j].rgbtGreen = tmpGreen;
            image[i][width - 1 - j].rgbtBlue = tmpBlue;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // Create a copy of image
    RGBTRIPLE copy[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {

            float tmpRed = 0;
            float tmpGreen = 0;
            float tmpBlue = 0;
            int count = 0;
            for (int x = -1; x < 2; x++)
            {
                for (int y = -1; y < 2; y++)
                {

                    if (i + x >= 0 && i + x < height && j + y >= 0 && j + y < width)
                    {
                        tmpRed += copy[i + x][j + y].rgbtRed;
                        tmpGreen += copy[i + x][j + y].rgbtGreen;
                        tmpBlue += copy[i + x][j + y].rgbtBlue;
                        count += 1;
                    }
                }
            }

            image[i][j].rgbtRed = round(tmpRed / (float) count);
            image[i][j].rgbtGreen = round(tmpGreen / (float) count);
            image[i][j].rgbtBlue = round(tmpBlue / (float) count);
        }
    }
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    // Create a copy of image
    RGBTRIPLE copy[height][width];

    // Define Sobel filters
    int gx[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
    int gy[3][3] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {

            float gxRed = 0;
            float gxGreen = 0;
            float gxBlue = 0;

            float gyRed = 0;
            float gyGreen = 0;
            float gyBlue = 0;

            for (int x = -1; x <= 1; x++)
            {
                for (int y = -1; y <= 1; y++)
                {
                    if (i + x >= 0 && i + x < height && j + y >= 0 && j + y < width)
                    {
                        gxRed += copy[i + x][j + y].rgbtRed * gx[x+1][y+1];
                        gxGreen += copy[i + x][j + y].rgbtGreen * gx[x+1][y+1];
                        gxBlue += copy[i + x][j + y].rgbtBlue * gx[x+1][y+1];

                        gyRed += copy[i + x][j + y].rgbtRed * gy[x+1][y+1];
                        gyGreen += copy[i + x][j + y].rgbtGreen * gy[x+1][y+1];
                        gyBlue += copy[i + x][j + y].rgbtBlue * gy[x+1][y+1];
                    }
                }
            }

            // Calculate the magnitude
            float calcRed = sqrt(gxRed * gxRed + gyRed * gyRed);
            float calcGreen = sqrt(gxGreen * gxGreen + gyGreen * gyGreen);
            float calcBlue = sqrt(gxBlue * gxBlue + gyBlue * gyBlue);

            if (calcRed > 255)
            {
                calcRed = 255;
            }

            if (calcGreen > 255)
            {
                calcGreen = 255;
            }

            if (calcBlue > 255)
            {
                calcBlue = 255;
            }

            image[i][j].rgbtRed = round(calcRed);
            image[i][j].rgbtGreen = round(calcGreen);
            image[i][j].rgbtBlue = round(calcBlue);
        }
    }
    return;
}
