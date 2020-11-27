# ShootingGame
PyQt5로 제작

키보드 컨트롤을 통해 적군을 피하거나 공격하여 살아남는 게임

## 조작 방법
### 방법 1
- 이동: W , A , S , D
- 공격
  - 총 : J 
  - 방어막 : K 
  - 순간이동 : L 
  - 폭탄 : ; 
- 궁극기: Space

### 방법 2
- 이동: 방향키 
- 공격
  - 총 : J 
  - 방어막 : H 
  - 순간이동 : G
  - 폭탄 : F 
- 궁극기: Space

## 게임요소
### 총
  - 총알 10개 (총알이 사라질 경우 충전됨)
  - 총으로 죽인 경우 점수와 에너지 1 증가

### 방어막
  - 쿨타임 10초
  - 범위 안에 있을 경우 적군을 다섯번 막아줌

### 순간이동
  - 쿨타임 10초
  - 흔적이 없을 경우 흔적을 남김
  - 흔적이 있을 경우 그곳으로 순간이동함

### 폭탄
  - 쿨타임 15초
  - 폭탄 범위 안에 있을 경우 속도가 느려짐
  - 적군은 폭탄 본체와 충돌하면 진행방향의 반대로 도망감
  - 5초 뒤 폭발함
  - 폭발 시 범위 안에있는 모든 것 (적군, 회복아이템 등) 을 죽임 
  - 폭발 시 플레이어는 50% 확률로 죽거나 hp가 초기상태로 리셋됨

### 궁극기 (타임슬로우)
  - 에너지 50을 채우면 사용가능 (총알이 금색으로 변함)
  - 5초동안 플레이어를 제외한 모든 것이 느려짐 (쿨타임은 지장을 받지 않음)

### 아이템
  - 3% 확률로 회복아이템 등장
  - 0.1% 확률로 모든 적군을 죽이는 아이템 등장

### 스테이지
  - 시간이 지날수록 (스테이지가 올라갈수록) 점점 적군이 많이나옴
