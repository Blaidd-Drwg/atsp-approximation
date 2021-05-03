library(ggplot2)
library(egg)

tbl_c <- read.csv("../../old_output/ftv170.atsp.c")
tbl_c$algo <- "Generalized Christofides algorithm"
tbl_t <- read.csv("../../old_output/ftv170.atsp.t")
tbl_t$algo <- "Generalized tree-doubling algorithm"

tbl <- rbind(tbl_c, tbl_t)

tbl$opt <- ave(tbl$tour_cost, tbl$algo, FUN=min)
tbl$aprox <- tbl$tour_cost / tbl$opt

p = ggplot(tbl,
       aes(
         x = aprox,
         y = kernel_size,
         color = algo)
) +
  geom_point() +
  xlab("approximation factor")+
  ylab("kernel size")

ggsave("output.pdf/ftp170.atsp.pdf", plot = p,
       width = 8, height = 5)
