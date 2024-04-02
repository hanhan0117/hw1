#include <cmath>

#include "GaussianblurFilter.h"

GaussianblurFilter::GaussianblurFilter(sc_module_name n) : sc_module(n)
{
  SC_THREAD(do_filter);
  sensitive << i_clk.pos();
  dont_initialize();
  reset_signal_is(i_rst, false);
}

// gaussianblur mask
const int mask[MASK_N][MASK_X][MASK_Y] = {{{1, 4, 7, 4, 1}, {4, 16, 26, 16, 4}, {7, 26, 41, 26, 7}, {4, 16, 26, 16, 4}, {1, 4, 7, 4, 1}}};

void GaussianblurFilter::do_filter()
{
  unsigned char grey[5][5] = {0};
  while (true)
  {

    for (unsigned int x = 0; x < MASK_X; ++x)
    {
      grey[x][MASK_Y - 1] = (i_r.read() + i_g.read() + i_b.read()) / 3;
    }

    for (unsigned int i = 0; i < MASK_N; ++i)
    {
      val[i] = 0;
    }
    for (unsigned int v = 0; v < MASK_Y; ++v)
    {
      for (unsigned int u = 0; u < MASK_X; ++u)
      {
        for (unsigned int i = 0; i != MASK_N; ++i)
        {
          val[i] += grey[u][v] * mask[i][u][v];
          if (v > 0 && v < MASK_Y)
          {
            grey[u][v - 1] = grey[u][v];
          }
        }
      }
    }

    double total = 0;
    for (unsigned int i = 0; i != MASK_N; ++i)
    {
      total += val[i];
    }
    int result = (int)(total / 273);
    o_result.write(result);
    wait(10); // emulate module delay
  }
}
