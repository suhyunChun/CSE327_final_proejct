import numpy as np

dt = 1.0/60
mu = np.array([0,0,0])
sig = np.array([[0.1,0,0],[0,0.1,0],[0,0,0.1]])

u = np.array([1,1,1])
A = np.array([[1,dt,0],
              [0,1,dt],
              [0,0,1]])
B = np.array([[1,0,0],
              [0,1,0],
              [0,0,1]])
Q = np.array([[0.05,0,0],
              [0,0.05,0],
              [0,0,0.05]])
H = np.array([[1,0,0],
              [0,1,0],
              [0,0,1]])
R = np.array([[0.4,0,0],
              [0,0.4,0],
              [0,0,0.4]])



def predict(A,B,Q,u, mu, sig):
    pred_mu = A @ mu + B @ u
    pred_sig = A @ sig @ A.T + Q
    return pred_mu, pred_sig

def update(H, R, Z, mu, sig):
    mean = Z - H @ mu
    cov = H @ sig @ H.T + R
    kal_gain = sig @ H.T @ np.linalg.inv(cov)
    new_mu = mu + kal_gain @ mean
    new_sig = sig - kal_gain @ H @ sig
    return new_mu, new_sig


def iterate(states,num):
    filtered =[]
    mu_cur = mu.copy()
    sig_cur = sig.copy()
    for aa in states:
        for i in range(num):
            pred_mu, pred_sig = predict(A,B,Q,u, mu_cur, sig_cur)
            mu_cur, sig_cur = update(H, R,aa , pred_mu, pred_sig)
            filtered.append(mu_cur)
    return np.array(filtered)
