source('helper.R')

library("scales")
library(tikzDevice)

tbl <- read.csv('./new_output.csv')

tbl_sym <- read.csv('./symmetry.csv')

tbl <- merge(tbl, tbl_sym, by = 'graph')

tbl$algo_named <- replace(tbl$algo, tbl$algo=='tree-doubling', 'Generalized tree-doubling')
tbl$algo_named <- replace(tbl$algo_named, tbl$algo_named=='christofides', 'Generalized Christofides')

tbl$kernel_size_rel <- tbl$kernel_size / tbl$graph_size

tbl_selection <- tbl[
  tbl$beta %in% c(1, 1.1, 2, 1.3, 1.5, 2) &
  #tbl$graph_size %in% c(100, 200, 300, 400, 500) &
  tbl$is_asymmetric == 1
  ,]

#tbl_selection$kernel_size_rel <- tbl_selection$kernel_size_rel+0.0001



p1 <- ggplot(tbl_selection,
             aes(
               x = cut_interval(graph_size,n=5),#as.factor(graph_size),
               y = kernel_size_rel,
               fill = as.factor(beta),
             )) +
  geom_boxplot(outlier.alpha = 0.5, position = position_dodge(.9)) +
  stat_summary(
    fun = mean,
    geom = "point",
    position = position_dodge(.9),
    shape = 5,
    size = 1.1
  ) +
  scale_fill_discrete(name = "$\\beta$") +
  scale_x_discrete(labels=c("50,\\\\100" ,"150,200", "250,300", "350,400", "450,500")) + 
  #  scale_y_continuous(trans=scales::pseudo_log_trans(sigma=0.001, base = 10)) + annotation_logticks(sides='l') +
  #  scale_y_log10() + annotation_logticks(sides='l') +
  facet_wrap( ~ algo_named, ncol = 2) + #, scales = 'free') +
  xlab("Graph size") +
  ylab("Parameter value (relative)") +
  theme(legend.position = "bottom",legend.margin = margin(0,0,0,0),legend.box.margin = margin(0,0,0,0),plot.margin = margin(0,0,0,0))
p1
ggsave(
  "output.pdf/new_output1.pdf",
  plot = p1,
  width = 8,
  height = 10
)
tikz(file = "output.tex/kernel_size1.tex", 
     width=4.8, height=3, base)
print(p1)
dev.off()

p2 <- ggplot(tbl_selection,
             aes(
               fill = as.factor(graph_size),
               y = kernel_size_rel,
               x = as.factor(beta),
             )) +
  geom_boxplot(outlier.alpha = 0.5, position = position_dodge(.9)) +
  stat_summary(
    fun = mean,
    geom = "point",
    position = position_dodge(.9),
    shape = 5,
    size = 4
  ) +
  scale_fill_discrete(name = "Graph size") +
  #scale_y_continuous(trans=scales::pseudo_log_trans(sigma=0.0001, base = 10)) + annotation_logticks(sides='l') +
  #scale_y_log10() + annotation_logticks(sides='l') +
  facet_wrap( ~ algo, ncol = 1, scales = 'free') +
  xlab("Beta") +
  ylab("Kernel size (relative)") +
  theme(legend.position = "bottom")
p2
ggsave(
  "output.pdf/new_output2.pdf",
  plot = p2,
  width = 8,
  height = 10
)
tikz(file = "output.tex/kernel_size2.tex", 
     width=4.8, height=7.1, base)
print(p2)
dev.off()

