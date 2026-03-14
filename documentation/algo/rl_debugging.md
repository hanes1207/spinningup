# Appendix: RL에서 디버깅 하는방법

## Shape을 계속 출력
```python
print(x.shape)
print(mu.shape)
print(log_std.shape)
```

특히 경계지점에서 찍기 \
e.g.
```
env → policy
policy → distribution
distribution → log_prob
```

```python
def gaussian_likelihood(x, mu, log_std):
    print("x:", x.shape)
    print("mu:", mu.shape)
    print("log_std:", log_std.shape)
```


## assert로 shape 강제하기
```python
assert x.dim() == 2
def gaussian_likelihood(x, mu, log_std):

    assert x.dim() == 2
    assert mu.shape == x.shape

    k = x.shape[1]
```
그러면 에러가 이렇게 바뀐다.
```
AssertionError: x must be [batch, dim]
```


## tensor 흐름을 종이에 그리기
RL policy 흐름은 항상 다음과 같다.
```
obs
 ↓
policy network
 ↓
mu
 ↓
distribution
 ↓
action sample
 ↓
log_prob
```

각 단계 shape:
```
obs        [batch, obs_dim]
mu         [batch, act_dim]
log_std    [act_dim] or [batch, act_dim]
action     [batch, act_dim]
log_prob   [batch]
```


## RL에서 특히 자주 생기는 문제
강화학습에서는 batch dimension이 자주 사라짐. \
원인:
```python
env.step()
→ single observation
→ shape = [obs_dim]
```

하지만 network는 
```
[batch, obs_dim]
```
을 기대한다.

그래서 rl 코드에는 항상
```python
if obs.dim() == 1:
    obs = obs.unsqueeze(0)
```
이 있다.


## 연구 코드에서 사용하는 helper
```python
def debug_shape(name, x):
    print(f"{name}: {x.shape}")
```