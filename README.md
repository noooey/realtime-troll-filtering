<h3 align='center'> Realtime Troll Filtering </h3>

<h1 align='center'> 실시간 악성 댓글 필터링 </h1>

<p align='center'> 머신러닝 기법을 이용하여 Youtube Live의 스트리밍에서 실시간으로 유해/악성 댓글을 필터링합니다. </p>

<h3 align='center'> 🤬  </h3>

<div align='center'>

<table>
    <thead>
        <tr>
            <th colspan="5"> ANTI-TROLL Team </th>
        </tr>
    </thead>
    <tbody>
        <tr>
          <tr>
            <td align='center'><a href="https://github.com/noooey"><img src="https://avatars.githubusercontent.com/u/66217855?v=4" width="100" height="100"></td>
            <td align='center'><a href="https://github.com/cherry031"><img src="https://avatars.githubusercontent.com/u/66215132?v=4" width="100" height="100"></td>
            <td align='center'><a href="https://github.com/YunHaaaa"><img src="https://avatars.githubusercontent.com/u/63325450?v=4" width="100" height="100"></td>
          </tr>
          <tr>
            <td align='center'>박규연</td>
            <td align='center'>심재민</td>
            <td align='center'>윤하은</td>
          </tr>
        </tr>
    </tbody>
</table>

</div>

&nbsp; 

## Intro
스트리밍 방송에서 실시간으로 발생하는 댓글에 대해 혐오성 여부를 판단하고, 필터링함으로써 댓글 청정도 개선

## Architecture
![image](https://github.com/noooey/Realtime-Troll-Filtering/assets/66217855/d0c38c62-01ff-45b0-bb27-684ceb3f8393)


## Data Processing
### Environment
- Docker
- EC2
### Process
1. 유튜브 댓글 크롤링 라이브러리인 **Pytchat**을 사용하여 라이브 방송의 댓글을 수집하여 Kafka 클러스터로 메세지를 보냅니다.
2. 메세지들은 해당 방송의 Topic에 적재됩니다.
3. Spark에서 Topic의 메세지들을 가져와 전처리를 진행합니다.
4. 전처리가 진행된 텍스트를 FastAPI로 요청을 보내 추론 결과를 받아옵니다.

## Models
### Environment
- Google Colab Pro+

### Dataset

### Experiments **(수정 중)**
|        |Accuracy|F1   |
|--------|--------|-----|
|KoBERT  |0.0%    |0.0% |
|SoongsilBERT|0.0%|0.0%|
|KoELECTRA|0.0%|0.0%  |

## Run
1. Make Youtube Developer Account and prepare API Key.
2. Create the `config.ini` file as shown below.
```ini
  # config.ini
  [youtube]
  api_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxx'
  ```

3. Execute with the following command **(수정 중)**

```shell
  $ make dependency
  $ make run
  ```
---

(학생설계형_팀형) Realtime-Troll-Filtering / ANTI-TROLL Team, 2023
