from abc import ABC, abstractmethod
import numpy as np
import matplotlib.pyplot as plt
import math

class CongestionControlAlgo(ABC):
    def __init__(self, init_window=0) -> None:
        super().__init__()
        self.alpha = 1
        self.beta = 0.5
        self.cur_win = init_window

    @abstractmethod
    def additiveIncrease(self):
        pass

    @abstractmethod
    def multiplicativeDecrease(self):
        pass

class TCP(CongestionControlAlgo):
    def __init__(self, init_window=0) -> None:
        super().__init__(init_window)

    def additiveIncrease(self):
        self.cur_win += self.alpha
        return self.cur_win

    def multiplicativeDecrease(self):
        self.cur_win *= self.beta
        return  self.cur_win

class HSTCP(CongestionControlAlgo):
    def __init__(self, init_window=0) -> None:
        super().__init__(init_window)
        # HighSpeed TCP params as suggested in RFC3649
        self.High_Window = 83000
        self.High_Decrease = 0.1
        self.Low_Window = 38

    def additiveIncrease(self):
        if self.cur_win <= self.Low_Window:
            self.alpha = 1
        else:
            bw = self.calc_beta(self.cur_win)
            aw = self.calc_alpha(self.cur_win, bw)

            if aw < 1:
                aw = 1

            self.alpha = aw
        self.cur_win += self.alpha
        
        return self.cur_win

    def multiplicativeDecrease(self):
        bw = self.calc_beta(self.cur_win)
        self.cur_win *= (1 - bw)
        return  self.cur_win

    def calc_beta(self, cur_win):
        return (self.High_Decrease - 0.5) * (math.log(cur_win) - math.log(self.Low_Window)) / (math.log(self.High_Window) - math.log(self.Low_Window)) + 0.5

    def calc_alpha(self, cur_win, beta):
        # p(w) = 0.078/w^1.2
        return (cur_win ** 2 * 2.0 * beta) / ((2.0 - beta) * cur_win ** 1.2 * 12.8)
    
class ScalableTCP(CongestionControlAlgo):
    def __init__(self, init_window=0) -> None:
        super().__init__(init_window)
        # Scalable TCP params
        self.Low_Window = 19
        self.beta = 0.125

    def additiveIncrease(self):
        if self.cur_win <= self.Low_Window:
            self.alpha = 1
        else:
            aw = self.calc_alpha(self.cur_win)
            self.alpha = aw
        self.cur_win += self.alpha
        
        return self.cur_win

    def multiplicativeDecrease(self):
        self.cur_win *= (1 - self.beta)
        return  self.cur_win

    def calc_alpha(self, cur_win):
        return cur_win * 0.01
    
class CUBIC(CongestionControlAlgo):
    def __init__(self, init_window=0) -> None:
        super().__init__(init_window)
        # CUBIC params
        self.C = 0.01
        self.beta = 0.2
        self.last_congestion = 0
        self.Max_Window = 0

    def additiveIncrease(self, cur_time):
        K = math.pow((1 - self.beta) * self.Max_Window / self.C, 1/3)
        self.cur_win = self.C * math.pow((cur_time - self.last_congestion) - K, 3) + self.Max_Window
        
        return self.cur_win

    def multiplicativeDecrease(self, cur_win, cur_time):
        self.Max_Window = max(self.Max_Window, cur_win)
        self.last_congestion = cur_time
        self.cur_win *= (1 - self.beta)
        return  self.cur_win
    

