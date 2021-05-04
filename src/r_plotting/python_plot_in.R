source('helper.R')

tbl <- read.csv("./old_output.csv")

tbl$opt <- ave(tbl$tour_cost, tbl$graph, FUN = min)
tbl$aprox <- tbl$tour_cost / tbl$opt

instances <-
  c(
    'br17',
    'ft53',
    'ft70',
    'ftv170',
    'ftv33',
    'ftv35',
    'ftv38',
    'ftv44',
    'ftv47',
    'ftv55',
    'ftv64',
    'ftv70',
    'kro124p',
    'p43',
    'rbg323',
    'rbg358',
    'rbg403',
    'rbg443',
    'ry48p'
  )

tbl1 <- tbl[tbl$graph %in% instances[1:8],]

p1 = ggplot(tbl1,
           aes(x = aprox,
               y = kernel_size,
               color = algo)) +
  facet_wrap(~graph, ncol=2, scales = 'free') +
  scale_color_discrete(name="Algorithm") +
  geom_point() +
  xlab("approximation factor") +
  ylab("kernel size")
p1
ggsave(
  "output.pdf/old_output1.pdf",
  plot = p1,
  width = 8,
  height = 10
)

tbl2 <- tbl[tbl$graph %in% instances[9:16],]

p2 = ggplot(tbl2,
            aes(x = aprox,
                y = kernel_size,
                color = algo)) +
  facet_wrap(~graph, ncol=2, scales = 'free') +
  scale_color_discrete(name="Algorithm") +
  geom_point() +
  xlab("approximation factor") +
  ylab("kernel size")
p2
ggsave(
  "output.pdf/old_output2.pdf",
  plot = p2,
  width = 8,
  height = 10
)

tbl3 <- tbl[tbl$graph %in% instances[17:19],]

p3 = ggplot(tbl3,
            aes(x = aprox,
                y = kernel_size,
                color = algo)) +
  facet_wrap(~graph, ncol=2, scales = 'free') +
  scale_color_discrete(name="Algorithm") +
  geom_point() +
  xlab("approximation factor") +
  ylab("kernel size")
p3
ggsave(
  "output.pdf/old_output3.pdf",
  plot = p3,
  width = 8,
  height = 5
)

