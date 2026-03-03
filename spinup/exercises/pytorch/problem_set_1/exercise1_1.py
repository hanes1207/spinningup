import torch
import numpy as np

"""

Exercise 1.1: Diagonal Gaussian Likelihood

Write a function that takes in PyTorch Tensors for the means and 
log stds of a batch of diagonal Gaussian distributions, along with a 
PyTorch Tensor for (previously-generated) samples from those 
distributions, and returns a Tensor containing the log 
likelihoods of those samples.

"""

def gaussian_likelihood(x, mu, log_std):
    """
    Args:
        x: Tensor with shape [batch, dim]
        mu: Tensor with shape [batch, dim]
        log_std: Tensor with shape [batch, dim] or [dim]

    Returns:
        Tensor with shape [batch]
    """
    #######################
    #                     #
    #   YOUR CODE HERE    #
    #                     #
    #######################
    # sigma = torch.exp(log_std)
    # log_likelihood = -0.5 * (torch.sum((((x - mu)**2 / sigma**2) + 2 * log_std), dim=1) + x.shape[1] * torch.log(2*torch.pi))
    # k = action dimension (여기서는 10)
    k = x.shape[1]
    
    # 1. 분자 부분: ((x - mu) / exp(log_std))^2
    # 2. 분모/상수 부분: 2 * log_std (로그 성질 이용)
    # 3. 파이 상수 부분: k * log(2 * pi)
    
    # 이 모든 걸 더한 뒤 -0.5를 곱합니다.
    # dim=1로 합치되, 결과가 [batch]가 되도록 keepdim은 쓰지 않습니다.
    pre_sum = ((x - mu) / torch.exp(log_std))**2 + 2 * log_std
    log_likelihood = -0.5 * (torch.sum(pre_sum, dim=1) + k * np.log(2 * np.pi))
    return log_likelihood


if __name__ == '__main__':
    """
    Run this file to verify your solution.
    """
    from spinup.exercises.pytorch.problem_set_1_solutions import exercise1_1_soln
    from spinup.exercises.common import print_result

    batch_size = 32
    dim = 10

    x = torch.rand(batch_size, dim)
    mu = torch.rand(batch_size, dim)
    log_std = torch.rand(dim)

    your_gaussian_likelihood = gaussian_likelihood(x, mu, log_std)
    true_gaussian_likelihood = exercise1_1_soln.gaussian_likelihood(x, mu, log_std)

    your_result = your_gaussian_likelihood.detach().numpy()
    true_result = true_gaussian_likelihood.detach().numpy()

    correct = np.allclose(your_result, true_result)
    print_result(correct)
