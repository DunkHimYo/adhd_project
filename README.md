# 게임 컨텐츠와  EEG를 이용한 CNN 기반 아동 ADHD 진단 시스템

- ADHD 환자의 대부분은 소아 남성이며 소아의 경우 판단력이 미숙하여 자가 진단 방식 뿐만 아니라 전산화된 테스트의 경우 장시간 측정하기 때문에 아동의 특성상 부적합 하며 정량화 뇌파 검사의 경우 주관적인 관점에서 진행되어 의사마다 진단 결과가 서로 상이할 수 있다는 문제가 생깁니다.
 - 이를 해결하기 위하여 뇌파 측정 장치로 부터 얻은 EEG데이터를 인공 신경망 알고리즘인 CNN을 이용해 객관적인 판단을 더하여 진단을 제공 할 수 있습니다.
 
### 정규 분포(걸린 시간)
- 정상인의 경우 대칭 구조가 나타남
- ADHD의 경우 평균이 중앙값보다 커서 좌로 치우쳐 진것을 확인 할 수 있음
- 정상인과 비교 하였을때 걸린 시간이 보다 오래 걸림
![waiting](https://github.com/DunkHimYo/adhd_project/blob/main/readMeImg/waiting%20time.jpg)

### 데이터 수집
- 최대 6 개월 동안 리탈린을 복용한 7 ~ 12세의 남녀 ADHD환자 61 명과 정신과적 장애, 간질 또는 고위험 행동에 대한 기록이 없는 정상인 60 명을 DSM-IV 기준에 따라 진단을 받았으며 시각적주의 작업을 기반으로 무작위 5 ~ 16 개 사이의 캐릭터의 수를 셈한 과정을 19 개 채널 (Fz, Cz, Pz, C3, T3, C4, T4, Fp1, Fp2, F3, F4, F7, F8, P3, P4, T5, T6, O1, O2)을 샘플링 주파수 128Hz로 기록
- ADHD의 경우 평균이 중앙값보다 커서 좌로 치우쳐 진것을 확인 할 수 있음
- 정상인과 비교 하였을때 걸린 시간이 보다 오래 걸림

| TOPOMAP | MRI |
| ------ | ------ |
|![chan_topo](https://github.com/DunkHimYo/adhd_project/blob/main/readMeImg/channel_topomap.png)|![mri](https://github.com/DunkHimYo/adhd_project/blob/main/readMeImg/mri.png)|

### 데이터 전처리

- Notch Filter

  가정용 전원에 의한 교류전기가 뇌파 기록에 섞여 50Hz에 큰 진폭이 발생하여 제거

| BEFORE | AFTER |
| ------ | ------ |
|![notch_before](https://github.com/DunkHimYo/adhd_project/blob/main/readMeImg/notch_filter_before.jpg)|![notch_after](https://github.com/DunkHimYo/adhd_project/blob/main/readMeImg/notch_filter_after.jpg)|

- Star(Sparse time artifact removal)

  각 채널에 일시적 발생한 로컬 아티팩트를 제거

| BEFORE | AFTER |
| ------ | ------ |
|![star_before](https://github.com/DunkHimYo/adhd_project/blob/main/readMeImg/star_before.png)|![star_after](https://github.com/DunkHimYo/adhd_project/blob/main/readMeImg/star_after.png)|

- ASR(Artifact Subspace Reconstruction)

  근육 발생 아티팩트의 공간을 재구성

| Musle Artifact |
| ------ |
|![muscle_artifact](https://github.com/DunkHimYo/adhd_project/blob/main/readMeImg/musle_artifact.jpg)|

| BEFORE | AFTER |
| ------ | ------ |
|![asr_before](https://github.com/DunkHimYo/adhd_project/blob/main/readMeImg/asr_before.jpg)|![asr_after](https://github.com/DunkHimYo/adhd_project/blob/main/readMeImg/asr_after.jpg)|


### 데이터 분석
- 최대 6 개월 동안 리탈린을 복용한 7 ~ 12세의 남녀 ADHD환자 61 명과 정신과적 장애, 간질 또는 고위험 행동에 대한 기록이 없는 정상인 60 명을 DSM-IV 기준에 따라 진단을 받았으며 시각적주의 작업을 기반으로 무작위 5 ~ 16 개 사이의 캐릭터의 수를 셈한 과정을 19 개 채널 (Fz, Cz, Pz, C3, T3, C4, T4, Fp1, Fp2, F3, F4, F7, F8, P3, P4, T5, T6, O1, O2)을 샘플링 주파수 128Hz로 기록
- ADHD의 경우 평균이 중앙값보다 커서 좌로 치우쳐 진것을 확인 할 수 있음
- 정상인과 비교 하였을때 걸린 시간이 보다 오래 걸림

| Time Correlation Compare |
| ------ |
|![chan_corr](https://github.com/DunkHimYo/adhd_project/blob/main/readMeImg/time_corr.png)|

| PSD Correlation Compare |
| ------ |
|![chan_corr](https://github.com/DunkHimYo/adhd_project/blob/main/readMeImg/freq_corr.png)|

| Abs Band Power Compare |
| ------ |
|![asr_before](https://github.com/DunkHimYo/adhd_project/blob/main/readMeImg/delta.png)|
|![asr_before](https://github.com/DunkHimYo/adhd_project/blob/main/readMeImg/theta.png)|
|![asr_before](https://github.com/DunkHimYo/adhd_project/blob/main/readMeImg/alpha.png)|
|![asr_before](https://github.com/DunkHimYo/adhd_project/blob/main/readMeImg/betaH.png)|
|![asr_before](https://github.com/DunkHimYo/adhd_project/blob/main/readMeImg/BetaM.png)|
|![asr_before](https://github.com/DunkHimYo/adhd_project/blob/main/readMeImg/betaL.png)|
|![asr_before](https://github.com/DunkHimYo/adhd_project/blob/main/readMeImg/gamma.png)|
|![asr_before](https://github.com/DunkHimYo/adhd_project/blob/main/readMeImg/total.png)|
