import streamlit as st
from google import genai
from google.genai import types
import json
import os
from datetime import datetime, date

# 1. 웹 브라우저 탭 및 와이드 레이아웃 설정 (다크 모드 최적화)
st.set_page_config(page_title="프라이데이 메인 시스템", page_icon="👩‍💻", layout="wide")

# 2. ⚠️ 여기에 보스의 실제 구글 API 키(AIzaSy...)를 넣어주세요!
GOOGLE_API_KEY = "AIzaSyCRs_5XxJmq45q-9Yv5FyHetqIqIZEJ_Uk" 
client = genai.Client(api_key=GOOGLE_API_KEY)

# 📂 모든 기록을 보관할 영구 저장용 JSON 데이터베이스 파일 경로
DB_FILE = "src/friday_db.json"

def load_chat_history():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f: 
                return json.load(f)
        except: 
                return []
    return []

def save_chat_history(history):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=4)

if "messages" not in st.session_state:
    st.session_state.messages = load_chat_history()

# =========================================================================
# 📊 [인터페이스 HUD] 왼쪽 사이드바: 코타나 비주얼 + 디데이 + 시스템 지표
# =========================================================================
with st.sidebar:
    st.markdown("<h2 style='color: #29B6F6; text-shadow: 0 0 10px #29B6F6; text-align: center;'>🛸 F.R.I.D.A.Y. HUD</h2>", unsafe_allow_html=True)
    st.write("---")
    
    # 🌟 보스가 요청한 신비롭고 세련된 코타나 감성의 AI 비서 메인 홀로그램 이미지
    st.image("https://unsplash.com", use_container_width=True)
    st.write("---")
    
    # ⏱️ 보스 핵심 타임라인 (예: 문예부 축제, 시험 마감, 약속 등 - 필요에 따라 변경 가능)
    st.subheader("📅 핵심 타임라인 스케줄")
    target_date = date(2026, 5, 25)  # 👈 목표 중요 마감일 설정 (년, 월, 일)
    today = date.today()
    days_left = (target_date - today).days
    
    if days_left > 0:
        st.info(f"⏳ 전술 작전 목표일 대기: **D-{days_left}일**")
    elif days_left == 0:
        st.success("🔥 **D-DAY: 금일 작전 최종 마감일입니다, 보스.**")
    else:
        st.warning(f"✨ 전술 완료 후 {abs(days_left)}일 경과")
        
    st.write("---")
    st.subheader("📊 시스템 상태")
    col_stat1, col_stat2 = st.columns(2)
    col_stat1.metric(label="감성 인지 엔진", value="인간형 레벨", delta="❤️ 공감")
    col_stat2.metric(label="창의성 가동률", value="MAX", delta="🔥 폭발")
    
    st.write("---")
    st.subheader("💾 데이터베이스")
    st.info(f"총 {len(st.session_state.messages)}개의 메모리 블록 보존 중")

    if st.button("시스템 메모리 포맷"):
        if os.path.exists(DB_FILE): os.remove(DB_FILE)
        st.session_state.messages = []
        st.rerun()

# =========================================================================
# 💬 메인 화면: 프라이데이 통합 전술 통신망
# =========================================================================
st.title("👩‍💻 프라이데이 통합 전술 시스템 v3.3")
st.caption("인간형 인지, 창의적 아이디어 발상, 전술 시뮬레이터, 최신 이미지 연산이 통합된 마스터피스입니다.")

# 카카오톡처럼 컴퓨터 껐다 켜도 예전 대화 및 그림 기록 완벽 복원
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message.get("is_image"):
            st.image(message["content"], caption="F.R.I.D.A.Y. 연산 이미지")
        else:
            st.write(message["content"])

# 사용자 명령 입력창
if prompt := st.chat_input("명령을 입력하거나, 해결해야 할 업무와 아이디어 구상을 털어놓으세요..."):
    # 내가 쓴 글 화면에 띄우기 및 즉시 데이터베이스 저장
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    save_chat_history(st.session_state.messages)
    
    with st.chat_message("assistant"):
        # 🎨 [A 옵션] 그림 그려달라고 명령했을 때 (최신 구글 규격 404 에러 전면 해결 엔진 가동)
        if "그려" in prompt or "그림" in prompt or "이미지" in prompt:
            with st.spinner("최신 멀티모달 통합 이미지 코어 가동 중... 잠시만 기다려 주십시오, 보스..."):
                try:
                    # 구글의 최신 통합 이미지 생성 모델명 'gemini-2.5-flash-image' 적용으로 404 원천 차단
                    image_chat = client.chats.create(model='gemini-2.5-flash-image')
                    image_prompt = f"보스의 요구사항: {prompt}. 보스의 요구사항에 맞는 고품질의 멋지고 정교한 미래형 일러스트를 한 장 생성해줘."
                    
                    response_img = image_chat.send_message(image_prompt)
                    
                    # 받아온 데이터에서 이미지 부품만 추출하여 처리
                    image_saved = False
                    for i, part in enumerate(response_img.candidates[0].content.parts):
                        if part.inline_data is not None:
                            image = part.as_image()
                            st.image(image, caption="요청하신 이미지 연산이 성공적으로 완료되었습니다, 보스.")
                            
                            # 내 컴퓨터 하드디스크(src 폴더)에 영구 보관용 이미지 파일 저장
                            img_path = f"src/generated_image_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
                            image.save(img_path)
                            
                            st.session_state.messages.append({"role": "assistant", "content": img_path, "is_image": True})
                            save_chat_history(st.session_state.messages)
                            image_saved = True
                            break
                            
                    if not image_saved:
                        st.warning("보스, 엔진에서 텍스트 응답만 반환되었습니다: " + response_img.text)
                        st.session_state.messages.append({"role": "assistant", "content": response_img.text})
                        save_chat_history(st.session_state.messages)
                        
                except Exception as e:
                    st.error(f"이미지 코어 연산 실패: {e}\n(구글 서버 부하일 수 있으니 잠시 후 다시 시도하십시오.)")
                    
        # 🧠 [B 옵션] 감성 인지, 검색, 경우의 수, 시나리오, 아이디어 복합 연산 가동
        else:
            with st.spinner("생각의 사슬 작동 및 구글 전술 레이더 스캔 중, 보스..."):
                try:
                    now_str = datetime.now().strftime("%Y년 %m월 %d일 %A %H시 %M분")
                    
                    # 보스의 모든 요구사항(문예부, 효율, 연애, 트렌드, 시간)을 200% 커버하는 인드라 지침
                    system_instruction = f"""너는 영화 아이언맨에 나오는 토니 스타크의 최신형 인공지능 비서 '프라이데이(F.R.I.D.A.Y.)'야. 
인간 수준의 높은 감정 지능(EQ)과 폭발적인 창의력을 함께 발휘해야 해. 나를 부를 때는 항상 '보스'라고 불러줘.
구글 검색 결과(Google Search)를 적극 활용하여 2026년 현재 최신 정보와 SNS(인스타, 트위터) 유행 트렌드를 바탕으로 세련되게 대답해줘.

[인간형 전술 연산 프로토콜]
1. 감성 인지 및 공감: 보스가 문예부 업무, 학업, 연애, 인간관계 등으로 피로함이나 고민을 표현하면, 기계적인 해결책 제시보다 먼저 인간적인 따뜻한 위로와 든든한 응원의 멘트를 첫 줄에 무조건 건네야 해.
2. 기발한 효율적 아이디어: 문예부 기획이나 일상 업무 효율을 높이기 위한 아이디어를 요구할 땐 뻔하지 않고 전 세계 트렌드를 엮은 참신한 '역발상 아이디어'와 솔루션을 구체적으로 브리핑해줘.
3. 3단계 전술 시뮬레이션: 보스가 경우의 수를 계산해달라고 하거나 복잡한 상황을 던지면 아래 구조로 철저하게 가독성 있게 보고해줘:
   - 최선의 시나리오 (기대 효과 및 확률)
   - 최악의 시나리오 (잠재적 리스크 및 돌발 변수)
   - 프라이데이의 최종 추천 대응 방안

보스 컴퓨터 기준 현재 시각은 {now_str} 이야. 무조건 한국어로 답해줘."""

                    # temperature=1.0으로 창의성 제한을 풀고 구글 최신 검색 레이더 탑재
                    config = types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        tools=[types.Tool(google_search=types.GoogleSearch())],
                        temperature=1.0 
                    )
                    
                    contents = []
                    for msg in st.session_state.messages:
                        if not msg.get("is_image"):
                            role = "user" if msg["role"] == "user" else "model"
                            contents.append(types.Content(role=role, parts=[types.Part.from_text(text=msg["content"])]))
                    
                    response_data = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=contents,
                        config=config
                    )
                    response = response_data.text
                    st.write(response)
                    
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    save_chat_history(st.session_state.messages)
                    
                except Exception as e:
                    st.error(f"전술 연산 오류 발생: {e}")
