#include <assert.h>
#include <dlfcn.h>
#include <stdarg.h>
#include <stdio.h>
#include <string.h>

static int fake_ioctl(int fd, unsigned long request, ...);
static void *test_dlsym(void *handle, const char *name) {
  (void)handle;
  assert(strcmp(name, "ioctl") == 0);
  return (void *)fake_ioctl;
}
#define dlsym test_dlsym
#include "isp-compat.c"
#undef dlsym

static unsigned long observed_request;
static struct mirror_vfe_input_cfg_new observed;
static void *observed_argument;
static int fake_ioctl(int fd, unsigned long request, ...) {
  va_list args;
  assert(fd == 42);
  va_start(args, request);
  observed_argument = va_arg(args, void *);
  va_end(args);
  observed_request = request;
  if (request == MIRROR_ISP_INPUT_CFG_NEW)
    memcpy(&observed, observed_argument, sizeof(observed));
  return 17;
}

int main(void) {
  struct mirror_vfe_input_cfg_old input;
  memset(&input, 0, sizeof(input));
  input.input_src = 0;
  input.input_pix_clk = 84000000;
  input.d.pix_cfg.camif_cfg.lines_per_frame = 1080;
  input.d.pix_cfg.camif_cfg.pixels_per_line = 1920;
  input.d.pix_cfg.camif_cfg.last_pixel = 1919;
  input.d.pix_cfg.camif_cfg.last_line = 1079;
  input.d.pix_cfg.fetch_engine_cfg.buf_width = 1920;
  input.d.pix_cfg.input_format = 8;
  assert(ioctl(42, MIRROR_ISP_INPUT_CFG_OLD, &input) == 17);
  assert(observed_request == MIRROR_ISP_INPUT_CFG_NEW);
  assert(observed.input_pix_clk == 84000000);
  assert(observed.d.pix_cfg.camif_cfg.last_pixel == 1919);
  assert(observed.d.pix_cfg.camif_cfg.last_line == 1079);
  assert(observed.d.pix_cfg.fetch_engine_cfg.buf_width == 1920);
  assert(observed.d.pix_cfg.input_format == 8);
  assert(observed.d.pix_cfg.camif_cfg.subsample_cfg.irq_subsample_period == 0);
  assert(observed.d.pix_cfg.camif_cfg.subsample_cfg.pixel_skip == 0);
  input.input_src = 1;
  input.d.rdi_cfg.cid = 3;
  input.d.rdi_cfg.frame_based = 1;
  assert(ioctl(42, MIRROR_ISP_INPUT_CFG_OLD, &input) == 17);
  assert(observed.input_src == 1 && observed.d.rdi_cfg.cid == 3);
  assert(observed.d.rdi_cfg.frame_based == 1);
  assert(ioctl(42, 0x1234UL, &input) == 17);
  assert(observed_request == 0x1234UL && observed_argument == &input);
  assert(af_haf_tof_update_func_tbl() == 0);
  puts("ISP ABI mapping and passthrough passed.");
  return 0;
}
