# -*- coding: utf-8 -*-
"""timesteppers.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1TgzhClGB3q2hVHyPaiOoM1MIQogBIJDB
"""
from scipy import sparse
import numpy as np
from math import factorial

class BackwardDifferentiationFormula:

    def __init__(self, u, L, steps):
        N = len(u)
        self.I = sparse.eye(N, N)  # Call superclass __init__ to initialize t
        self.t = 0
        self.iter = 0
        self.u1 = u
        self.steps = steps
        self.L = L


    def mat_solve(self, A_sparse, b):
        A_sparse_csc = A_sparse.tocsc()

        LU = spla.splu(A_sparse_csc, permc_spec='NATURAL')

        x = LU.solve(b)
        return x

    def make_stencil(self, steps):

        # assume constant grid spacing
        i = np.arange(self.steps + 1)[:, None]
        j = np.arange(self.steps + 1)[None, :]
        S = (1/factorial(i))*((j*self.dt)**i)

        b = np.zeros(self.steps + 1)
        b[1] = 1

        stencil = scipy.linalg.solve(S, b)
        self.coef = self.dt/stencil[0]
        self.stencil = (-stencil/stencil[0])*self.dt

    def step(self, dt, sol_list):

        sol = self.mat_solve(self.oper_mat,(self.stencil[1]*self.sol_list[self.iter+1] + self.stencil[2]*self.sol_list[self.iter]))
        self.sol_list.append(sol)

        self.t += dt
        self.iter += 1

    def evolve(self, dt, time):

        self.dt= dt
        self.make_stencil(self.steps)
        self.oper_mat = self.I - (self.coef*self.L.matrix)
        self.init_sol = self.mat_solve(self.oper_mat,self.u1)

        sol_list = []
        sol_list.append(self.u1)
        sol_list.append(self.init_sol)
        self.sol_list = sol_list

        while self.t < time - 1e-8:
            self.step(dt,sol_list)

        self.u = self.sol_list[self.iter]
