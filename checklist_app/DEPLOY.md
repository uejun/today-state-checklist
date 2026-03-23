# 当日状態確認チェックシート AWS App Runner デプロイ手順

## 前提

- AWS CLIが設定済み
- Docker がインストール済み
- Google Sheetsの準備が完了済み（スプレッドシート名: `香り評価_当日状態確認`）

---

## 1. ECRリポジトリの作成

```bash
aws ecr create-repository --repository-name checklist-app --region ap-northeast-1
```

出力されるリポジトリURIをメモする（例: `123456789012.dkr.ecr.ap-northeast-1.amazonaws.com/checklist-app`）

---

## 2. Dockerイメージのビルドとプッシュ

```bash
cd checklist_app

# ECRにログイン
aws ecr get-login-password --region ap-northeast-1 | docker login --username AWS --password-stdin 123456789012.dkr.ecr.ap-northeast-1.amazonaws.com

# ビルド & プッシュ
docker build -t checklist-app .
docker tag checklist-app:latest 123456789012.dkr.ecr.ap-northeast-1.amazonaws.com/checklist-app:latest
docker push 123456789012.dkr.ecr.ap-northeast-1.amazonaws.com/checklist-app:latest
```

`123456789012` は自分のAWSアカウントIDに置き換える。

---

## 3. App Runner用のIAMロール作成

App RunnerがECRからイメージをpullするためのロールが必要。

```bash
aws iam create-role \
  --role-name AppRunnerECRAccessRole \
  --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Principal": {"Service": "build.apprunner.amazonaws.com"},
      "Action": "sts:AssumeRole"
    }]
  }'

aws iam attach-role-policy \
  --role-name AppRunnerECRAccessRole \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSAppRunnerServicePolicyForECRAccess
```

---

## 4. サービスアカウントJSONの準備

GCPのサービスアカウントJSONファイルの内容を**1行のJSON文字列**に変換する。

```bash
cat service-account.json | jq -c .
```

出力された文字列を次のステップで使用する。

---

## 5. App Runnerサービスの作成

AWSコンソールから作成する場合:

1. **App Runner** コンソールを開く
2. 「サービスを作成」をクリック
3. ソース:
   - **コンテナレジストリ**: Amazon ECR
   - **イメージURI**: 手順2でプッシュしたURI
   - **ECRアクセスロール**: `AppRunnerECRAccessRole`
4. 設定:
   - **ポート**: `8501`
   - **CPU**: 1 vCPU
   - **メモリ**: 2 GB
5. 環境変数:
   - **キー**: `GCP_SERVICE_ACCOUNT_JSON`
   - **値**: 手順4で生成した1行JSON文字列
6. 「作成とデプロイ」をクリック

---

## 6. デプロイ後の確認

App Runnerが提供するデフォルトドメイン（`https://xxxxx.ap-northeast-1.awsapprunner.com`）にアクセスして動作確認。

---

## イメージの更新

コードを変更した場合:

```bash
cd checklist_app
docker build -t checklist-app .
docker tag checklist-app:latest 123456789012.dkr.ecr.ap-northeast-1.amazonaws.com/checklist-app:latest
docker push 123456789012.dkr.ecr.ap-northeast-1.amazonaws.com/checklist-app:latest
```

App Runnerコンソールで「デプロイ」をクリック、または自動デプロイが有効なら自動で反映される。
