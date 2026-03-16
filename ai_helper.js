/**
 * 校园模拟系统 - DeepSeek AI 辅助模块
 * 负责管理所有的提示词(Prompts)以及与大模型的网络通信
 */

const AIHelper = {
    apiKey: "sk-b8ad34dc116b4019bef6e47240bfa81c",
    endpoint: "https://api.deepseek.com/chat/completions",

    // 1. 根据姓名推测性别偏向
    async guessGender(name) {
        const prompt = `你是一个学籍系统辅助AI。请分析中文姓名"${name}"，判断其偏向男性还是女性，或者两者皆有可能。
        必须严格返回一个合法的 JSON 对象，不要包含任何 markdown 代码块符号或多余的说明文字。
        返回格式必须精确如下：
        {
            "gender": "男" 或 "女" 或 "未知",
            "reason": "简短的一句话原因，例如'包含典型的男性用字'或'该名字属于中性，男女皆可'等"
        }`;
        return this.callAPI(prompt);
    },

    // 2. 生成全量校园模拟数据
    async generateStudentData(name, gender, studentId) {
        const prompt = `请为一个名为"${name}"的${gender}性高中生生成一套完整的校园模拟数据。必须严格返回一个合法的 JSON 对象，不要包含任何 markdown 代码块符号或多余的说明文字。返回结构如下：
        {
          "user": { "student_id": "${studentId}", "real_id": "随机生成一个合法的18位中国身份证号", "name": "${name}", "class_name": "高二(3)班", "gender": "${gender}", "ethnicity": "汉族或其他", "position": "班长等职务", "enrollment": "2023年9月", "politics": "共青团员", "avatar": "https://api.dicebear.com/7.x/notionists/svg?seed=${Math.random().toString(36).substring(7)}" },
          "news": [ { "tag": "⭐ 头条新闻", "title": "具有校园特色的新闻标题", "desc": "新闻简短描述", "date": "2024-03-15", "circle_color_1": "bg-accentRed", "circle_color_2": "bg-accentYellow" }, { "tag": "🎨 校园活动", "title": "艺术节等新闻", "desc": "描述", "date": "2024-03-10", "circle_color_1": "bg-accentGreen", "circle_color_2": "bg-accentBlue" } ],
          "archives": {
            "academic": [ { "title": "高二年级期中考试", "date": "2024.01", "tag": "期中", "totalScore": 620, "totalMax": 750, "gradeRank": 5, "subjects": [ { "name": "语文", "score": 115, "avg": 105, "change": "↑ 2", "changeColor": "text-accentRed" }, { "name": "数学", "score": 135, "avg": 110, "change": "↑ 5", "changeColor": "text-accentRed" } ]} ],
            "health": [ { "title": "秋季体质健康测试", "date": "2023.11", "result_summary": "身体各项指标良好，建议保持适量运动。", "details": [ { "item": "身高 (cm)", "value": "175.5", "status": "正常", "color": "text-accentGreen" }, { "item": "体重 (kg)", "value": "65.2", "status": "正常", "color": "text-accentGreen" }, { "item": "双眼视力", "value": "4.8/4.9", "status": "正常", "color": "text-accentGreen" } ]} ],
            "library": [ { "title": "人类简史", "author": "尤瓦尔", "borrow_date": "2024.02.15", "due_date": "2024.03.15", "status": "借阅中", "days_left": 15, "cover": "https://covers.openlibrary.org/b/id/8780917-L.jpg" } ],
            "award": [ { "type": "Honor", "item": "省级三好学生", "date": "2023.12", "issuer": "省教育厅", "description": "在过去的一年中品学兼优，特发此证以资鼓励。" } ]
          }
        }`;
        return this.callAPI(prompt);
    },

    // 核心调用方法
    async callAPI(promptStr) {
        const response = await fetch(this.endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.apiKey}`
            },
            body: JSON.stringify({
                model: 'deepseek-chat',
                messages: [
                    { role: 'system', content: 'You are a data API. You must return ONLY valid JSON.' },
                    { role: 'user', content: promptStr }
                ],
                response_format: { type: "json_object" }
            })
        });

        if (!response.ok) throw new Error("API 请求失败");
        const jsonResponse = await response.json();
        
        let contentText = jsonResponse.choices[0].message.content.trim();
        // 清理可能含有的 markdown JSON 标识
        if (contentText.startsWith("```json")) {
            contentText = contentText.replace(/^```json\n?/, '').replace(/\n?```$/, '');
        }
        
        return JSON.parse(contentText);
    }
};

window.AIHelper = AIHelper;