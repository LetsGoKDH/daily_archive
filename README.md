# Daily Papers

arXiv, Interspeech, ICASSP, IEEE, ACL 등에서 매일 새 논문을 수집하고 AI 요약(한/영)을 생성하는 정적 사이트.

## 실행

```bash
pip install -r requirements.txt
export OPENAI_API_KEY="your-key"
python scripts/run_daily.py
```

`site/index.html`을 브라우저에서 열면 됨.

## 자동화

GitHub Actions가 매일 06:00 KST에 자동 빌드. Repository Settings > Secrets에 `OPENAI_API_KEY` 추가 필요.
