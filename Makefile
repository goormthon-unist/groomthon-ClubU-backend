.PHONY: format commit-format

format:
	@echo "🎨 Black 포맷팅 실행 중..."
	black .
	@echo "✅ 포맷팅 완료!"

commit-format:
	@echo "🚀 포맷팅 후 자동 커밋..."
	black .
	git add .
	git commit -m "style: Apply black formatting"
	@echo "🎉 완료!"

help:
	@echo "사용 가능한 명령어:"
	@echo "  make format        - Black 포맷팅 실행"
	@echo "  make commit-format - 포맷팅 후 자동 커밋"
