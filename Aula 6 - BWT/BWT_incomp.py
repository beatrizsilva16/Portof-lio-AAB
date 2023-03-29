# -*- coding: utf-8 -*-

class BWT:
    
    def __init__(self, seq = "", buildsufarray = False):
        self.bwt = self.build_bwt(seq, buildsufarray) 
    
    def set_bwt(self, bw):
        self.bwt = bw

    def build_bwt(self, text, buildsufarray = False):
        ls = []
        # ...

#        if buildsufarray:
#            self.sa = []
#            for i in range(len(ls)):
#                stpos = ls[i].index("$")
#                self.sa.append(len(text)-stpos-1)
        return res    
    
    def inverse_bwt(self):
        firstcol = self.get_first_col()
        res = ""
        c = "$" 
        occ = 1
        for i in range(len(self.bwt)):
            # ....
        return res        
 
    def get_first_col (self):
        firstcol = []
        # ...
        return firstcol
        
    def last_to_first(self):
        res = []
        #...
        return res

    def bw_matching(self, patt):
        lf = self.last_to_first()
        res = []
        top = 0
        bottom = len(self.bwt)-1
        flag = True
        while flag and top <= bottom:
            if patt != "":
                symbol = patt[-1]
                patt = patt[:-1]
                lmat = self.bwt[top:(bottom+1)]
                if symbol in lmat:
                    topIndex = lmat.index(symbol) + top
                    bottomIndex = bottom - lmat[::-1].index(symbol)
                    top = lf[topIndex]
                    bottom = lf[bottomIndex]
                else: flag = False
            else: 
                for i in range(top, bottom+1): res.append(i)
                flag = False            
        return res        
 
    def bw_matching_pos(self, patt):
        res = []
        #...
        return res
 
# auxiliary
 
def find_ith_occ(l, elem, index):
    # ...
    return -1 

      
def test():
    seq = "TAGACAGAGA$"
    bw = BWT(seq)
    print (bw.bwt)
#    print (bw.last_to_first())
#    print (bw.bw_matching("AGA"))


def test2():
    bw = BWT("")
    bw.set_bwt("ACG$GTAAAAC")
    print (bw.inverse_bwt())

def test3():
    seq = "TAGACAGAGA$"
    bw = BWT(seq, True)
    print("Suffix array:", bw.sa)
#    print(bw.bw_matching_pos("AGA"))

test()
#test2()
#test3()

