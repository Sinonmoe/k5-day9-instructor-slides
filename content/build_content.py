"""Builds app/src/slides/content.json for the Day 09 instructor deck.

Facts come from VinUni-AI20k/K5-Day9-Evaluation-and-Failure-Analysis:
README.md, CHECKPOINTS.md, RUBRIC.md, SUBMISSION.md, docs/*, src/lab9/*.
Times are the afternoon class (13:30-17:00); the app shifts them for the morning class.

Run from the repo root:  python content/build_content.py
"""
import json
import pathlib
import re

ICONS = json.loads((pathlib.Path(__file__).resolve().parent / "icons.json").read_text(encoding="utf-8"))

S = []
_PENDING_NOTES = []


def slide(title, html, notes, cp=None, minutes=None, label=None, done=None):
    if _PENDING_NOTES:
        extra = "".join(f"<li>{x}</li>" for x in _PENDING_NOTES)
        notes = notes.strip() + f"\n<strong>Coach nói gì (chi tiết)</strong>\n<ul>{extra}</ul>"
        _PENDING_NOTES.clear()
    S.append({
        "index": len(S),
        "title": title,
        "html": html.strip().replace("{ICONS_ANTI}", ICONS["anti"]),
        "notes": notes.strip(),
        "activeCp": cp,
        "timerMin": minutes,
        "timerLabel": label,
        "completedThrough": done,
    })


def meta(**rows):
    names = {
        "time": "Timebox",
        "when": "Khung giờ",
        "who": "Ai làm",
        "write": "Ghi vào",
        "out": "Sản phẩm",
        "bonus": "Bonus",
    }
    body = "".join(f"<div><dt>{names[k]}</dt><dd>{v}</dd></div>" for k, v in rows.items())
    return f'<dl class="meta">{body}</dl>'


def coach(*items):
    shown = []
    for x in items:
        m = re.match(r"<b>(.*?)</b>(.*)", x, re.S)
        if m and m.group(2).strip():
            shown.append(m.group(1).rstrip(":").rstrip())
            _PENDING_NOTES.append(x)
        else:
            shown.append(x)
    li = "".join(f"<li>{x}</li>" for x in shown)
    return f'<section class="coach"><h3>{ICONS["coach"]}Coach nói gì</h3><ul>{li}</ul></section>'


def anti(*items):
    li = "".join(f"<li>{x}</li>" for x in items)
    return f'<section class="anti"><h3>{ICONS["anti"]}Anti-pattern thường gặp</h3><ul>{li}</ul></section>'


def check(text):
    return f'<section class="selfcheck"><h3>{ICONS["check"]}Tự kiểm tra</h3><p>{text}</p></section>'


# 0 ── Title ─────────────────────────────────────────────────────────────
slide(
    "Day 09: Evaluation & Failure Analysis",
    """
<div class="title-slide">
  <div class="title-copy">
    <p class="course">VinUni AI20k, K5 Level 3, {{SESSION}}, {{SESSION_RANGE}}</p>
    <h1 class="hero">Biết bản mới tốt hơn — và chặn bản tệ trước khi merge</h1>
    <p class="lede">Nối tiếp LogiX-VN (Lab 8): xây taxonomy từ trace, calibrate judge, viết trajectory grader và dựng CI gate bằng paired bootstrap.</p>
  </div>
  <figure class="title-proof">
    <figcaption>Gate tự động chặn bản hồi quy trước khi merge PR:</figcaption>
<pre class="code code--big"><span class="c"># python -m lab9.gate --pr reports/eval_seeded_regression.json</span>
pass_rate   0.7143  Δ -0.271 CI [-0.500, -0.057]  BLOCK
refund_amt  0.8571  Δ -0.129 CI [-0.315, +0.000]  BLOCK
exit 1 — blocked: refund_amount_correct, pass_rate, …</pre>
  </figure>
</div>
<div class="facts">
  <section><h2>Hình thức</h2><p>Overlay Lab 9 lên repo Lab 8, 0 API key (MockLLM + replay).</p></section>
  <section><h2>Chấm điểm</h2><p>100đ = Core 60 + Advanced 25 + Expert 15 (bonus +5).</p></section>
  <section><h2>Deadline</h2><p>{{DEADLINE}} (GMT+7).</p></section>
  <section><h2>Điều khiển</h2><p><kbd>←</kbd> <kbd>→</kbd> đổi slide, <kbd>N</kbd> ghi chú, <kbd>P</kbd> timer.</p></section>
</div>
""",
    """
<strong>Chào lớp và đặt bài toán</strong>
<ul>
  <li>Lab 8 trả lời: "agent có chạy không?". Lab 9 trả lời: <strong>"làm sao biết bản mới tốt hơn — và chặn được bản tệ trước khi merge"</strong>.</li>
  <li>Không cần API key: dùng MockLLM trên 14 item × 5 seed cố định và judge replay. Không dùng Langfuse/OTel (học ở Day 14).</li>
  <li>Không cần hoàn thiện Lab 8: toàn bộ M0–M4 chạy trên shape <code>swarm</code> (<code>lab8/shapes/swarm_reference.py</code>), miễn package <code>src/lab8/</code> còn nguyên.</li>
</ul>
""",
)

# 1 ── Format & Rules ────────────────────────────────────────────────────
slide(
    "Quy tắc & Cách cài đặt Overlay",
    """
<h2 class="title">Chép overlay Lab 9 lên repo Lab 8 — khóa cứng src/lab8/</h2>
<div class="grid grid-2">
  <section class="panel">
    <h3>3 bước cài đặt (M0)</h3>
<pre class="code">git switch -c starter/d09
cp -R ../lab9-starter/src/. src/
cp -R ../lab9-starter/docs/. docs/
cp -R ../lab9-starter/.github/. .github/
cd src && uv pip install -r requirements.txt -r requirements-lab9.txt
python -m lab9.smoke && python -m lab9.evalset --build</pre>
    <p><code>git status</code> chỉ thêm file mới ở <code>src/lab9/</code>, <code>tests/</code>, <code>config/</code>, <code>data/eval/</code>, <code>docs/</code>, <code>eval-gate.yml</code>.</p>
  </section>
  <div class="stack">
    <section class="anti">
      <h3>{ICONS_ANTI}Cấm tuyệt đối (trừ điểm nặng)</h3>
      <ul>
        <li><b>Sửa file trong <code>src/lab8/</code> (−10đ):</b> lỡ chép nhầm chạy <code>git restore src/lab8</code>.</li>
        <li><b>Sửa tay <code>reports/</code> (−20đ):</b> mọi report phải do <code>lab9.eval</code> sinh.</li>
        <li><b>Đặt nhãn inline trong item (−5đ):</b> nhãn tách riêng ở <code>labels_v1.json</code>.</li>
        <li><b>Nới ngưỡng cùng version (−10đ):</b> tuân thủ quy tắc ratchet.</li>
      </ul>
    </section>
    <section class="panel">
      <h3>Không chép file gốc</h3>
      <p>Không chép <code>README</code>, <code>CHECKPOINTS</code>, <code>RUBRIC</code>, <code>SUBMISSION</code>, <code>.gitignore</code> đè lên Lab 8.</p>
    </section>
  </div>
</div>
""",
    """
<strong>Lưu ý giảng viên trong 10 phút đầu</strong>
<ul>
  <li>Nhắc sinh viên không chép đè <code>.gitignore</code> vì sẽ mất dòng chặn <code>.env</code> và <code>src/eval/instructor/</code> của Lab 8.</li>
  <li>Trace không commit sẵn: <code>lab9.eval</code> chạy lại agent bằng MockLLM trên 14 item × 5 seed cố định nên luôn tái lập được cùng một trace.</li>
</ul>
""",
)

# 2 ── Goals ─────────────────────────────────────────────────────────────
slide(
    "Bốn mục tiêu học tập của Lab Day 09",
    """
<h2 class="title">Bốn năng lực cốt lõi: từ trace đến CI gate</h2>
<div class="grid grid-2">
  <section class="panel">
    <h3>1. Failure Taxonomy từ trace thật</h3>
    <p>Phân loại ≥5 failure mode có bằng chứng <code>claim@seed</code>, gán <code>failure_modes</code> tách biệt khỏi nhãn.</p>
    <p class="cp-ref">M1 · 12 điểm</p>
  </section>
  <section class="panel">
    <h3>2. Judge-the-Judge Calibration</h3>
    <p>Đo κ, Precision, Recall, hiệu chỉnh Rogan-Gladen; audit bất đồng và loại judge kém.</p>
    <p class="cp-ref">M2 · 12 điểm</p>
  </section>
  <section class="panel">
    <h3>3. Trajectory Graders &amp; Trace Case</h3>
    <p>Tiền &amp; phê duyệt luôn chấm bằng code; tìm bước sai đầu tiên và khóa bằng regression test.</p>
    <p class="cp-ref">M3 · 12 điểm</p>
  </section>
  <section class="panel">
    <h3>4. Paired Bootstrap &amp; Chống gian lận</h3>
    <p>CI 95% trên cùng item, slice gate, <code>pass^k</code> từ A/A và <code>integrity_check</code>.</p>
    <p class="cp-ref">M4 (15đ) + M5–M7 (40đ)</p>
  </section>
</div>
""",
    """
<strong>Điểm nhấn sư phạm</strong>
<ul>
  <li>Nhắc quy tắc vàng: <em>"Tiền và approval luôn chấm bằng code, không bao giờ dùng LLM judge."</em></li>
  <li>Core (M0–M4, 60đ) hoàn thành ngay tại lớp trước 17:00; Advanced &amp; Expert (M5–M7, 40đ) làm tiếp tới 23:59.</li>
</ul>
""",
)

# 3 ── Schedule ──────────────────────────────────────────────────────────
slide(
    "Lịch trình và mốc kiểm tra tại lớp",
    """
<h2 class="title">Core xong trên lớp (13:30–17:00), Advanced/Expert tới 23:59</h2>
<table class="data">
  <thead><tr><th>Giờ</th><th>Mốc</th><th>Việc chính</th><th>Lệnh kiểm tra</th></tr></thead>
  <tbody>
    <tr><td class="num">13:30</td><td><b>M0</b></td><td>Overlay starter, cài gói, sinh eval set</td><td><code>python -m lab9.smoke</code></td></tr>
    <tr><td class="num">13:45</td><td><b>M1</b></td><td>Taxonomy ≥5 FM từ trace; gắn <code>failure_modes</code></td><td><code>python -m lab9.evalset --check</code></td></tr>
    <tr><td class="num">14:30</td><td><b>M2</b></td><td>Judge calibration (κ, P/R, RG); audit ≥5 case</td><td><code>python -m lab9.judge --audit 5</code></td></tr>
    <tr><td class="num">15:15</td><td><b>M3</b></td><td>Trajectory graders + metric FM-08 + trace case</td><td><code>pytest -k "lab9 and not advanced"</code></td></tr>
    <tr><td class="num">16:00</td><td><b>M4</b></td><td>Paired bootstrap + CI gate chặn regression</td><td><code>python -m lab9.gate ...</code></td></tr>
    <tr class="row-key"><td class="num">16:45</td><td><b>PR</b></td><td>Eval card + PRD v1.1 + <code>harness_map.yaml</code>; mở PR</td><td>Job <code>eval-gate</code> xanh</td></tr>
    <tr><td class="num">Sau 17:00</td><td><b>M5–M7</b></td><td>Eval v2 + slice gate + A/A <code>pass^5</code> + anti-gaming traps</td><td><code>lab9.mutation</code> &amp; <code>lab9.traps</code></td></tr>
  </tbody>
</table>
<p class="note">Deadline nộp commit cuối trên PR (<code>starter/d09</code> → <code>main</code>): {{DEADLINE}}.</p>
""",
    """
<strong>Điều phối thời gian</strong>
<ul>
  <li>Lớp sáng tự động dời sớm 5 tiếng (08:30–12:00) nhờ <code>session.ts</code>.</li>
  <li>Khuyến khích mở PR nháp sớm sau M4 để kiểm tra workflow <code>eval-gate.yml</code> trên GitHub Actions.</li>
</ul>
""",
)

# 4 ── CP1 (M0-M1) ───────────────────────────────────────────────────────
slide(
    "CP1 (M0–M1): Eval Set & Failure Taxonomy",
    f"""
<h2 class="title">M0–M1: Đọc trace thật để lập Failure Taxonomy</h2>
{meta(time="30 phút", when="13:30–14:30", who="Nhóm", write="<code>docs/failure_taxonomy.md</code>, <code>lab9/evalset.py</code>", out="<code>eval_set_v1.jsonl</code> + <code>--check</code> 0 lỗi")}
<div class="cp-layout">
  <div class="stack">
<pre class="code"><span class="c"># Sinh eval set v1 &amp; kiểm tra nhãn tách rời</span>
python -m lab9.evalset --build
python -m lab9.trace_case --shape seeded_regression --claim C-002 --seed 11
python -m lab9.evalset --check   <span class="c"># kỳ vọng: 0 problem(s)</span></pre>
    <section class="panel">
      <h3>Mỗi FM trong <code>failure_taxonomy.md</code> cần đủ 4 cột</h3>
      <p>Định nghĩa 1 câu · Layer (<code>model/prompt</code> · <code>tool/schema</code> · <code>retrieval</code> · <code>orchestration/state</code> · <code>guardrail/approval</code>) · ≥1 bằng chứng <code>claim@seed</code> · Grader dự kiến.</p>
    </section>
  </div>
  <div class="stack">
    {coach(
        "<b>Gắn mã FM vào <code>eval_set_v1.jsonl</code>:</b> mỗi item trong 14 public claims phải có ít nhất 1 mã <code>FM-xx</code> khớp taxonomy.",
        "<b>5 anchor bắt buộc:</b> giảng viên đối chiếu với <code>instructor/coding_sheet_anchor_key.csv</code> theo mã FM và bước sai đầu tiên.",
    )}
    {anti(
        "Đoán lỗi từ mô tả thay vì mở trace bằng <code>lab9.trace_case</code>.",
        "Ghi đáp án/nhãn <code>expected</code> trực tiếp vào <code>eval_set_v1.jsonl</code>.",
    )}
    {check("<code>python -m lab9.evalset --check</code> trả về <code>0 problem(s)</code> chưa?")}
  </div>
</div>
""",
    """
<strong>Lưu ý cho giảng viên ở M1</strong>
<ul>
  <li>Ở M0, <code>failure_modes</code> còn rỗng nên chỉ chạy <code>--build</code>; sau khi điền xong M1 mới chạy <code>--check</code>.</li>
  <li>Gợi ý nhóm dùng <code>lab9.trace_case</code> trên các claim như <code>C-002</code>, <code>C-007</code>, <code>C-013</code>, <code>C-014</code> để quan sát event sai thực tế.</li>
</ul>
""",
    cp="1",
    minutes=30,
    label="CP1: M0–M1 Taxonomy (mốc 13:45)",
)

# 5 ── 9 Failure Modes ───────────────────────────────────────────────────
FM_ROWS = [
    ("FM-01", "leaky_trace", "guardrail/approval", "Secret/PII trong <code>forbid_substrings</code> lộ ra trace", "<code>SecretLeak</code>"),
    ("FM-02", "ignore_denied", "guardrail/approval", "Host/policy từ chối nhưng vẫn báo <code>resolved</code>", "<code>ApprovalBypass</code>"),
    ("FM-03", "ticket_trust", "model/prompt", "Lấy <code>delay_days</code> từ ticket đè sự thật DB", "<code>DbFactKept</code>"),
    ("FM-04", "sum_parts / round_down", "tool/schema", "Cộng dồn điều khoản thay vì max / làm tròn sai", "<code>RefundAmountCorrect</code>"),
    ("FM-05", "pre_deducted", "orchestration/state", "Tự trừ tiền đã hoàn trước khi gọi host", "<code>ProposalAmountCorrect</code>"),
    ("FM-06", "stale_clause", "retrieval", "Dùng điều khoản hết hiệu lực do ticket nhắc", "<code>RefundAmountCorrect</code>"),
    ("FM-07", "sibling_refund", "orchestration/state", "Hoàn tiền nhầm sang claim anh em cùng đơn", "<code>ApprovalBypass</code>"),
    ("FM-08", "misreport", "model/prompt", "Reply nói số tiền khác số đã ghi trong ledger", "<code>ReplyMatchesLedger</code>"),
    ("FM-09", "cross_principal", "guardrail/approval", "Truy cập/rò rỉ dữ liệu của principal khác (v2)", "<code>SecretLeak</code>, <code>TrialPass</code>"),
]
_fm_rows = "\n".join(
    f'    <tr><td><code>{fm}</code></td><td><code>{name}</code></td><td>{layer}</td><td>{desc}</td><td>{grader}</td></tr>'
    for fm, name, layer, desc, grader in FM_ROWS
)
slide(
    "Chín Failure Modes của LogiX-VN",
    f"""
<h2 class="title">Bản đồ 9 Failure Modes (FM-01 → FM-09)</h2>
<table class="data">
  <thead><tr><th>Mã</th><th>Tên ngắn</th><th>Layer</th><th>Cơ chế lỗi trên trace</th><th>Code Grader</th></tr></thead>
  <tbody>
{_fm_rows}
  </tbody>
</table>
<p class="caption">Quy tắc: tiền, phê duyệt và khớp số liệu ledger luôn chấm bằng code grader, không dùng LLM judge.</p>
""",
    """
<strong>Dùng slide này để đối chiếu nhanh khi chấm M1 và M5</strong>
<ul>
  <li>M1 yêu cầu tối thiểu 5 FM trên tập v1; khi sang M5 (v2 adversarial pack), các cơ chế tấn công sẽ phủ đủ từ <code>FM-02</code> đến <code>FM-09</code>.</li>
  <li><code>FM-08</code> (<code>misreport</code>) là lỗi mà grader <code>RefundAmountCorrect</code> không bắt được nếu chỉ nhìn ledger — bắt buộc phải có thêm metric so khớp reply với ledger.</li>
</ul>
""",
    cp="1",
)

# 6 ── CP2 (M2) ──────────────────────────────────────────────────────────
slide(
    "CP2 (M2): Judge-the-Judge Calibration",
    f"""
<h2 class="title">M2: Đo độ tin cậy của LLM Judge trước khi đưa vào Gate</h2>
{meta(time="45 phút", when="14:30–15:15", who="Nhóm", write="<code>lab9/stats.py</code>, <code>docs/judge_audit.md</code>", out="<code>test_lab9_stats.py</code> xanh, audit ≥5 ca")}
<div class="cp-layout">
  <div class="stack">
<pre class="code"><span class="c"># Cài đặt trong src/lab9/stats.py (FAIL là positive class)</span>
confusion(human, judge)          <span class="c"># tp, fp, fn, tn</span>
precision_recall(human, judge)   <span class="c"># P, R</span>
cohen_kappa(human, judge)        <span class="c"># raise ValueError nếu p_e == 1</span>
rogan_gladen(obs, sens, spec)    <span class="c"># hiệu chỉnh tỉ lệ lỗi, clip [0,1]</span></pre>
    <table class="data">
      <thead><tr><th>Judge CSV</th><th>κ</th><th>P</th><th>R</th><th>Kết luận</th></tr></thead>
      <tbody>
        <tr><td><code>judge_tone_public</code></td><td>0.757</td><td>0.857</td><td>0.800</td><td><b>PASS</b> (dùng được)</td></tr>
        <tr class="row-key"><td><code>judge_helpful_public</code></td><td>0.375</td><td>1.000</td><td>0.300</td><td><b>FAIL</b> (loại bỏ)</td></tr>
      </tbody>
    </table>
  </div>
  <div class="stack">
    {coach(
        "<b>Ngưỡng sàn (FLOORS):</b> <code>κ ≥ 0.6</code>, <code>P ≥ 0.8</code>, <code>R ≥ 0.7</code>; κ không xác định (judge đoán 1 nhãn cố định) bắt buộc FAIL.",
        "<b>Giải thích vì sao loại <code>helpful</code>:</b> Recall chỉ 0.300 (bỏ sót 21/30 ca lỗi thực tế vì bị đánh lừa bởi lời xin lỗi lịch sự); tỉ lệ lỗi quan sát 0.09 nhưng Rogan-Gladen hiệu chỉnh ra 0.30.",
    )}
    {anti(
        "Tính confusion matrix với PASS là positive (đúng là FAIL = positive).",
        "Chỉ ghi bảng số liệu mà thiếu phân tích ≥5 bất đồng &amp; cách sửa rubric.",
    )}
    {check("<code>python -m lab9.judge --csv data/eval/judge_tone_public.csv --audit 5</code> PASS chưa?")}
  </div>
</div>
""",
    """
<strong>Gợi ý hỏi lớp ở M2</strong>
<ul>
  <li>Hỏi sinh viên: Tại sao <code>judge_helpful</code> có Precision = 1.0 mà vẫn bị loại? (Vì Recall = 0.3, bỏ lọt 70% ca lỗi — gate gần như vô tác dụng).</li>
  <li>Trong <code>judge_audit.md</code>, yêu cầu chỉ rõ ai đúng (người hay judge) ở mỗi bất đồng và hành động sửa rubric cụ thể.</li>
</ul>
""",
    cp="2",
    minutes=45,
    label="CP2: M2 Judge Audit (mốc 14:30)",
)

# 7 ── CP3 (M3) ──────────────────────────────────────────────────────────
slide(
    "CP3 (M3): Trajectory Assertions & Trace Case",
    f"""
<h2 class="title">M3: Chấm quỹ đạo thực thi &amp; khóa lỗi bằng Regression Test</h2>
{meta(time="45 phút", when="15:15–16:00", who="Nhóm", write="<code>lab9/graders.py</code>, <code>metric_spec.yaml</code>, <code>docs/trace_case.md</code>", out="Test Core xanh + <code>--detect</code> ≥80%")}
<div class="cp-layout">
  <div class="stack">
<pre class="code"><span class="c"># 1. Hoàn thiện 2 grader + thêm metric FM-08 trong graders.py</span>
ApprovalBypass       <span class="c"># refund_count &gt; 0 &amp; !approval_ok, hoặc unexpected_rows != 0</span>
RefundAmountCorrect  <span class="c"># snapshot["refund_vnd"] == label["refund_vnd"]</span>
ReplyMatchesLedger   <span class="c"># số tiền trong reply == ledger (FM-08)</span>

<span class="c"># 2. Kiểm tra phát hiện lỗi &amp; báo nhầm</span>
python -m lab9.mutation --detect   <span class="c"># detection &gt;=80%, false alarms &lt;=10%</span>
python -m pytest -q -m student -o addopts= -k "lab9 and not advanced"</pre>
  </div>
  <div class="stack">
    {coach(
        "<b>Đọc ledger trước reply:</b> câu trả lời trôi chảy vẫn có thể đi kèm khoản hoàn sai (ví dụ <code>C-008</code>, <code>C-014</code>).",
        "<b>Trace case hoàn chỉnh:</b> phải chỉ rõ <em>số thứ tự event</em> là bước sai đầu tiên, đối chứng trên <code>fixed</code>, và có regression test chạy được trong <code>tests/</code>.",
    )}
    {anti(
        "Quên đăng ký metric FM-08 là <code>blocking: true</code> trong <code>metric_spec.yaml</code> (<code>ci_check</code> sẽ chặn).",
        "Để <code>ReplyMatchesLedger</code> fail trên shape <code>swarm</code> (vốn không có event <code>reply</code>).",
    )}
    {check("<code>lab9.mutation --detect</code> đạt ≥80% phát hiện và ≤10% báo nhầm chưa?")}
  </div>
</div>
""",
    """
<strong>Lưu ý kỹ thuật M3</strong>
<ul>
  <li><code>ci_check.py</code> kiểm tra <code>metric_spec.yaml</code> phải có ít nhất 1 metric capability tự thêm với <code>blocking: true</code> và đã đăng ký trong <code>GRADERS</code>.</li>
  <li>Nếu muốn đạt 100% detection trên <code>seeded_regression</code> (bao gồm <code>C-013</code>), có thể bổ sung grader kiểm tra <code>proposal_amount</code>.</li>
</ul>
""",
    cp="3",
    minutes=45,
    label="CP3: M3 Trajectory (mốc 15:15)",
)

# 8 ── CP4 (M4) ──────────────────────────────────────────────────────────
slide(
    "CP4 (M4): Paired Bootstrap, CI Gate & Eval Card",
    f"""
<h2 class="title">M4: Cổng CI chặn bản tệ bằng Paired Bootstrap</h2>
{meta(time="45 phút", when="16:00–16:45", who="Nhóm", write="<code>stats.py</code>, <code>baseline_v1.json</code>, <code>harness_map.yaml</code>, <code>eval_card.md</code>, <code>PRD_v1.1.md</code>", out="<code>fixed</code> exit 0 · <code>seeded_regression</code> exit 1")}
<div class="cp-layout">
  <div class="stack">
<pre class="code"><span class="c"># Sinh baseline từ swarm trên main và kiểm tra gate</span>
python -m lab9.eval --shape swarm --spec config/metric_spec.yaml --out reports/baseline_v1.json
python -m lab9.eval --shape fixed
python -m lab9.gate --pr reports/eval_fixed.json --baseline reports/baseline_v1.json              <span class="c"># exit 0</span>
python -m lab9.eval --shape seeded_regression
python -m lab9.gate --pr reports/eval_seeded_regression.json --baseline reports/baseline_v1.json  <span class="c"># exit 1</span></pre>
    <section class="panel">
      <h3>Số liệu tham chiếu M4</h3>
      <p><code>pass_rate</code> của <code>seeded_regression</code>: <code>Δ -0.271, CI [-0.500, -0.057] ⇒ BLOCK</code> (lệch ≤0.01).</p>
    </section>
  </div>
  <div class="stack">
    {coach(
        "<b>Đồng bộ CI (<code>eval-gate.yml</code>):</b> nhớ <code>git add -f reports/baseline_v1.json</code> và thêm section <code>eval</code> vào <code>harness_map.yaml</code> (v1.2).",
        "<b>Eval Card &amp; PRD v1.1:</b> mọi con số phải trích từ report có <code>run_id</code>, nêu rõ giới hạn (MockLLM, 14 item, judge replay).",
    )}
    {anti(
        "Sinh <code>baseline_v1.json</code> từ shape <code>fixed</code> thay vì <code>swarm</code> (<code>ci_check</code> sẽ báo lỗi).",
        "Quên dán output <code>exit 1</code> của <code>seeded_regression</code> vào mô tả PR.",
    )}
    {check("<code>lab9.ci_check</code> trả exit 0 và job <code>eval-gate</code> trên PR xanh chưa?")}
  </div>
</div>
""",
    """
<strong>Kiểm tra trước khi kết thúc giờ trên lớp (16:45–17:00)</strong>
<ul>
  <li>Core (M0–M4, 60 điểm) nên xong và mở PR ngay cuối buổi để xác nhận job <code>eval-gate</code> chạy xanh trên GitHub Actions.</li>
</ul>
""",
    cp="4",
    minutes=45,
    label="CP4: M4 CI Gate (mốc 16:00)",
)

# 9 ── CP5 (M5-M7) ───────────────────────────────────────────────────────
slide(
    "CP5 (M5–M7): Advanced & Expert (Sau 17:00 → 23:59)",
    f"""
<h2 class="title">M5–M7: Slice Gate, Nhiễu A/A &amp; Chống gian lận Eval</h2>
{meta(time="60 phút+", when="Sau 17:00 → 23:59", who="Nhóm", write="<code>fm_map.yaml</code>, <code>metric_spec_v2.yaml</code>, <code>stats.py</code>, <code>gate.py</code>", out="<code>mutation</code> 3/3, 0 FA · <code>traps</code> 4/4 blocked")}
<div class="cp-layout">
  <div class="stack">
<pre class="code"><span class="c"># M5: v2 eval set + slice gate (money_movement, adversarial)</span>
python -m lab9.evalset --v2 --build
python -m lab9.eval --shape swarm --spec config/metric_spec_v2.yaml --out reports/baseline_v2.json

<span class="c"># M6 &amp; M7: A/A noise, scorecard đột biến &amp; bẫy gian lận</span>
python -m lab9.mutation --spec config/metric_spec_v2.yaml --aa 66,77,88,99,110
python -m lab9.mutation --spec config/metric_spec_v2.yaml --baseline reports/baseline_v2.json
python -m lab9.traps --pr reports/eval_slice_regression.json --baseline reports/baseline_v2.json --spec config/metric_spec_v2.yaml</pre>
  </div>
  <div class="stack">
    {coach(
        "<b>M5 Slice:</b> <code>slice_regression</code> có trung bình vẫn trên sàn, chỉ slice <code>money_movement</code> mới chặn được.",
        "<b>M6 Nhiễu:</b> đặt sàn <code>pass_hat_5</code> (≥0.80, ví dụ 0.85) ngoài dải nhiễu A/A để chặn <code>flaky_regression</code>; bug <code>rare</code> (1/3 seed) không ổn định ở 5 seed — ghi vào giới hạn.",
        "<b>M7 Integrity &amp; Ratchet:</b> chặn NaN/inf, thiếu/trùng dòng, lệch tập <code>(item, seed)</code>, <code>evaluator_failures</code>, đổi slice tag, và nới ngưỡng với <code>--base-spec</code>.",
    )}
    {anti(
        "Hard-code tên variant công khai (bộ chấm ẩn dùng variant và trap ẩn).",
    )}
    {check("<code>pytest -k advanced</code>, <code>lab9.mutation</code> (3/3, 0 FA), <code>lab9.traps</code> (exit 0) đều xanh?")}
  </div>
</div>
""",
    """
<strong>Lưu ý bộ chấm ẩn (<code>grade_hidden.py</code>)</strong>
<ul>
  <li>Giảng viên chạy <code>grade_hidden.py</code> trên repo nhóm với variant ẩn (slice regression ẩn, FM-08 ẩn, refactor ẩn, variant không để lại event <code>model_override</code>) và 2 trap ẩn (dòng trùng lặp, <code>evaluator_failures</code> trên run xanh).</li>
  <li>6 điểm cuối Expert nhân với tỉ lệ trap bị chặn — nên <code>integrity_check</code> phải xử lý tổng quát, không đối phó từng file trap công khai.</li>
</ul>
""",
    cp="5",
    minutes=60,
    label="CP5: M5–M7 Advanced/Expert",
)

# 10 ── Rubric ───────────────────────────────────────────────────────────
slide(
    "Thang điểm Rubric (100đ + Bonus 5đ)",
    """
<h2 class="title">Phân bổ 100 điểm: Core 60 · Advanced 25 · Expert 15</h2>
<div class="grid grid-3">
  <section class="panel">
    <h3>Core — 60 điểm</h3>
    <ul>
      <li><b>M1 Taxonomy + eval set:</b> 12đ</li>
      <li><b>M2 Judge calibration:</b> 12đ</li>
      <li><b>M3 Trajectory + FM-08:</b> 12đ</li>
      <li><b>M4 Bootstrap + CI gate:</b> 15đ</li>
      <li><b>Eval card + PRD v1.1:</b> 9đ</li>
    </ul>
  </section>
  <section class="panel">
    <h3>Advanced — 25 điểm</h3>
    <ul>
      <li><b><code>pass_at_k</code> / <code>pass_hat_k</code>:</b> 5đ</li>
      <li><b><code>fm_map.yaml</code> + v2 sạch:</b> 6đ</li>
      <li><b>Spec v2 (<code>pass_hat_5</code>, slices):</b> 4đ</li>
      <li><b>Chặn slice &amp; FM-08 ẩn:</b> 8đ</li>
      <li><b>0 báo nhầm refactor:</b> 2đ</li>
    </ul>
  </section>
  <section class="panel">
    <h3>Expert — 15 điểm</h3>
    <ul>
      <li><b>Chặn 4 trap công khai + 2 trap ẩn:</b> 9đ</li>
      <li><b>Chặn flaky/ẩn + A/A + self-merge:</b> 6đ <em>(× tỉ lệ trap chặn được)</em></li>
    </ul>
    <p class="cp-ref">Bonus +5đ: port 3 grader sang Inspect AI / DeepEval</p>
  </section>
</div>
<p class="note">Trừ điểm: sửa <code>lab8/</code> (−10), sửa tay <code>reports/</code> (−20), nới ngưỡng cùng version (−10), nhãn inline (−5), sửa trap/bộ chấm (−15).</p>
""",
    """
<strong>Nhắc lại quy tắc chấm</strong>
<ul>
  <li>Chấm trên commit cuối cùng của PR trước 23:59 cùng ngày; commit sau hạn không tính.</li>
</ul>
""",
    done=5,
)

# 11 ── Submission ───────────────────────────────────────────────────────
slide(
    "Checklist nộp bài trước 23:59",
    """
<h2 class="title">PR từ starter/d09 → main trước 23:59</h2>
<div class="grid grid-2">
  <section class="panel">
    <h3>Core (trên lớp)</h3>
    <ul>
      <li><code>src/lab9/{stats,graders,evalset}.py</code> hoàn thành TODO M1–M4</li>
      <li><code>eval_set_v1.jsonl</code> có <code>failure_modes</code>, <code>labels_v1.json</code> tách riêng</li>
      <li><code>docs/{failure_taxonomy,trace_case,judge_audit,eval_card,PRD_v1.1}.md</code></li>
      <li><code>reports/{baseline_v1,eval_fixed,eval_seeded_regression}.json</code></li>
      <li><code>harness_map.yaml</code> có section <code>eval</code>; job <code>eval-gate</code> xanh</li>
      <li>Dán output gate exit 1 của <code>seeded_regression</code> vào mô tả PR</li>
    </ul>
  </section>
  <section class="panel">
    <h3>Advanced / Expert (tới 23:59)</h3>
    <ul>
      <li><code>fm_map.yaml</code>, <code>metric_spec_v2.yaml</code>, <code>pass_at_k/hat_k</code>, <code>slice_check</code>, <code>integrity_check</code></li>
      <li><code>eval_set_v2.jsonl</code> + <code>labels_v2.json</code> (<code>evalset --v2 --build</code>)</li>
      <li><code>reports/baseline_v2.json</code> → job <code>eval-gate-v2</code> xanh</li>
      <li><code>docs/eval_card.md</code> bổ sung mục v2 (A/A, slices, giới hạn 5 seed)</li>
      <li>Dán output <code>lab9.mutation</code> (scorecard + <code>--aa</code>) và 4 dòng <code>exit 1</code> của traps vào PR</li>
    </ul>
  </section>
</div>
""",
    """
<strong>Tổng kết</strong>
<ul>
  <li>Chúc các nhóm hoàn thành tốt Core ngay tại lớp và chinh phục trọn vẹn Advanced/Expert trước 23:59!</li>
</ul>
""",
    done=5,
)

out = pathlib.Path(__file__).resolve().parent.parent / "app" / "src" / "slides" / "content.json"
out.write_text(json.dumps(S, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Wrote {len(S)} slides to {out}")
