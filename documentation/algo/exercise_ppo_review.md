# Exercise code ppo review



## matmul compile error
```
(spinningup) root@7da0021d5679:~/spinningup# python spinup/exercises/pytorch/problem_set_1/exercise1_2.py
Logging data to /tmp/experiments/1773408492/progress.txt
Saving config:

{
    "ac_kwargs":        {
        "hidden_sizes": [
            64
        ]
    },
    "actor_critic":     "functools.partial(<class 'spinup.exercises.pytorch.problem_set_1.exercise1_2_auxiliary.ExerciseActorCritic'>, actor=<class '__main__.MLPGaussianActor'>)",
    "clip_ratio":       0.2,
    "env_fn":   "<function <lambda> at 0xffff769d4430>",
    "epochs":   20,
    "gamma":    0.99,
    "lam":      0.97,
    "logger":   {
        "<spinup.utils.logx.EpochLogger object at 0xffff769d5520>":     {
            "epoch_dict":       {},
            "exp_name": null,
            "first_row":        true,
            "log_current_row":  {},
            "log_headers":      [],
            "output_dir":       "/tmp/experiments/1773408492",
            "output_file":      {
                "<_io.TextIOWrapper name='/tmp/experiments/1773408492/progress.txt' mode='w' encoding='UTF-8'>":        {
                    "mode":     "w"
                }
            }
        }
    },
    "logger_kwargs":    {
        "output_dir":   "/tmp/experiments/1773408492"
    },
    "max_ep_len":       1000,
    "pi_lr":    0.0003,
    "save_freq":        10,
    "seed":     0,
    "steps_per_epoch":  4000,
    "target_kl":        0.01,
    "train_pi_iters":   80,
    "train_v_iters":    80,
    "vf_lr":    0.001
}
/root/miniforge3/envs/spinningup/lib/python3.9/site-packages/gym/logger.py:30: UserWarning: WARN: Box bound precision lowered by casting to float32
  warnings.warn(colorize('%s: %s'%('WARN', msg % args), 'yellow'))

Number of parameters:    pi: 386,        v: 385

Traceback (most recent call last):
  File "/root/spinningup/spinup/exercises/pytorch/problem_set_1/exercise1_2.py", line 130, in <module>
    ppo(env_fn = lambda : gym.make('InvertedPendulum-v2'),
  File "/root/spinningup/spinup/algos/pytorch/ppo/ppo.py", line 300, in ppo
    a, v, logp = ac.step(torch.as_tensor(o, dtype=torch.float32))
  File "/root/spinningup/spinup/exercises/pytorch/problem_set_1/exercise1_2_auxiliary.py", line 47, in step
    pi, _ = self.pi(obs)
  File "/root/miniforge3/envs/spinningup/lib/python3.9/site-packages/torch/nn/modules/module.py", line 1518, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
  File "/root/miniforge3/envs/spinningup/lib/python3.9/site-packages/torch/nn/modules/module.py", line 1527, in _call_impl
    return forward_call(*args, **kwargs)
  File "/root/spinningup/spinup/exercises/pytorch/problem_set_1/exercise1_2.py", line 102, in forward
    mu = self.mu_net(obs)
  File "/root/miniforge3/envs/spinningup/lib/python3.9/site-packages/torch/nn/modules/module.py", line 1518, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
  File "/root/miniforge3/envs/spinningup/lib/python3.9/site-packages/torch/nn/modules/module.py", line 1527, in _call_impl
    return forward_call(*args, **kwargs)
  File "/root/miniforge3/envs/spinningup/lib/python3.9/site-packages/torch/nn/modules/container.py", line 215, in forward
    input = module(input)
  File "/root/miniforge3/envs/spinningup/lib/python3.9/site-packages/torch/nn/modules/module.py", line 1518, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
  File "/root/miniforge3/envs/spinningup/lib/python3.9/site-packages/torch/nn/modules/module.py", line 1527, in _call_impl
    return forward_call(*args, **kwargs)
  File "/root/miniforge3/envs/spinningup/lib/python3.9/site-packages/torch/nn/modules/linear.py", line 114, in forward
    return F.linear(input, self.weight, self.bias)
RuntimeError: could not create a primitive descriptor for a matmul primitive
```

해결방법: \
spinningup은 docker+CPU instruction error가 날 수 있다. \
torch 2.1.0 보다 torch 1.13.1 이 더 안정적이다.




## 코드 구현하면서 사람들이 틀리는 포인트 3개
1. log_std.expand_as(mu)
2. obs.unsqueeze(0)
3. action batch dimension 유지

나는 3번 포인트에서 걸렸다...
```
(spinningup) root@7da0021d5679:~/spinningup# python spinup/exercises/pytorch/problem_set_1/exercise1_2.py
Logging data to /tmp/experiments/1773410715/progress.txt
Saving config:

{
    "ac_kwargs":        {
        "hidden_sizes": [
            64
        ]
    },
    "actor_critic":     "functools.partial(<class 'spinup.exercises.pytorch.problem_set_1.exercise1_2_auxiliary.ExerciseActorCritic'>, actor=<class '__main__.MLPGaussianActor'>)",
    "clip_ratio":       0.2,
    "env_fn":   "<function <lambda> at 0xffff9d3c4430>",
    "epochs":   20,
    "gamma":    0.99,
    "lam":      0.97,
    "logger":   {
        "<spinup.utils.logx.EpochLogger object at 0xffff9d3ca970>":     {
            "epoch_dict":       {},
            "exp_name": null,
            "first_row":        true,
            "log_current_row":  {},
            "log_headers":      [],
            "output_dir":       "/tmp/experiments/1773410715",
            "output_file":      {
                "<_io.TextIOWrapper name='/tmp/experiments/1773410715/progress.txt' mode='w' encoding='UTF-8'>":        {
                    "mode":     "w"
                }
            }
        }
    },
    "logger_kwargs":    {
        "output_dir":   "/tmp/experiments/1773410715"
    },
    "max_ep_len":       1000,
    "pi_lr":    0.0003,
    "save_freq":        10,
    "seed":     0,
    "steps_per_epoch":  4000,
    "target_kl":        0.01,
    "train_pi_iters":   80,
    "train_v_iters":    80,
    "vf_lr":    0.001
}
/root/miniforge3/envs/spinningup/lib/python3.9/site-packages/gym/logger.py:30: UserWarning: WARN: Box bound precision lowered by casting to float32
  warnings.warn(colorize('%s: %s'%('WARN', msg % args), 'yellow'))

Number of parameters:    pi: 386,        v: 385

tensor([-0.0543])
Traceback (most recent call last):
  File "/root/spinningup/spinup/exercises/pytorch/problem_set_1/exercise1_2.py", line 130, in <module>
    ppo(env_fn = lambda : gym.make('InvertedPendulum-v2'),
  File "/root/spinningup/spinup/algos/pytorch/ppo/ppo.py", line 300, in ppo
    a, v, logp = ac.step(torch.as_tensor(o, dtype=torch.float32))
  File "/root/spinningup/spinup/exercises/pytorch/problem_set_1/exercise1_2_auxiliary.py", line 49, in step
    logp_a = pi.log_prob(a)
  File "/root/spinningup/spinup/exercises/pytorch/problem_set_1/exercise1_2.py", line 71, in log_prob
    return exercise1_1.gaussian_likelihood(value, self.mu, self.log_std)
  File "/root/spinningup/spinup/exercises/pytorch/problem_set_1/exercise1_1.py", line 33, in gaussian_likelihood
    k = x.shape[1]
IndexError: tuple index out of range
```

해설:
``` python
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
    print(x)
    k = x.shape[1]
    pre_sum = ((x - mu) / (torch.exp(log_std) + EPS)) ** 2 + 2 * log_std
    log_likelihood = -0.5 * (torch.sum(pre_sum, dim=1) + k * np.log(2 * np.pi))

    return log_likelihood
```
위에서 print(x) 찍힌 것을 보면 `tensor([-0.0543])`로 들어온다. 

gaussian_likelihood 문제가 아니라 action tensor shape 문제입니다. \
a = pi.sample()이 batch dimension을 유지하지 않고 반환하고 있는 것.


`DiagonalGaussianDistribution.sample()`에서
```python
pi = self.mu + torch.exp(self.log_std) * torch.randn_like(self.mu)
```
이라고 되어있는데, mu shape이 상황에 따라 두 가지가 됩니다. \
 - 정상:
    ```
    mu.shape = [batch, act_dim]
    ex) [1,1]
    ```
 - 하지만 ac.step() 내부에서 squeeze가 발생하면
    ```
    mu.shape = [act_dim]
    ex) [1]
    ```
그래서 sample()이 `tensor([-0.0543])`를 반환합니다.

해결 방법 (정석) \
sample()에서 batch dimension을 강제로 유지합니다. \
수정: 
```python
def sample(self):

    mu = self.mu
    log_std = self.log_std

    if mu.dim() == 1:
        mu = mu.unsqueeze(0)

    std = torch.exp(log_std)

    if std.dim() == 1:
        std = std.unsqueeze(0)

    pi = mu + std * torch.randn_like(mu)

    return pi
```
