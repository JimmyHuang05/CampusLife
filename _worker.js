/**
 * CampusLife - EdgeOne 边缘函数 (Pages 适配版)
 * 采用 ES Module 语法，支持 _worker.js 自动部署和环境变量注入
 */

const corsHeaders = {
    'Access-Control-Allow-Origin': '*', // 生产环境建议改为您的真实域名
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
};

export default {
    async fetch(request, env) {
        // 1. 处理 CORS 预检请求
        if (request.method === 'OPTIONS') {
            return new Response(null, { headers: corsHeaders });
        }

        if (request.method !== 'POST') {
            return new Response('Method Not Allowed', { status: 405, headers: corsHeaders });
        }

        try {
            const url = new URL(request.url);
            const body = await request.json();
            
            // 从 env 对象中安全获取您在 EdgeOne 控制台配置的环境变量
            const apiKey = env.DEEPSEEK_API_KEY; 
            
            if (!apiKey) {
                throw new Error("API Key 未配置，请检查 EdgeOne 环境变量设置");
            }

            let prompt = '';

            // 2. 路由分发
            if (url.pathname.endsWith('/api/guess-gender')) {
                prompt = `你是一个学籍系统辅助AI。请分析中文姓名"${body.name}"，判断其偏向男性还是女性，或者两者皆有可能。必须严格返回一个合法的 JSON 对象，不要包含任何 markdown 代码块符号或多余的说明文字。
                返回格式必须精确如下：
                {"gender": "男" 或 "女" 或 "未知", "reason": "简短的一句话原因"}`;
            } 
            else if (url.pathname.endsWith('/api/generate-student')) {
                prompt = `请为一个名为"${body.name}"的${body.gender}性高中生生成一套完整的校园模拟数据。必须严格返回一个合法的 JSON 对象，不要包含任何 markdown 代码块符号或多余的说明文字。返回结构如下：
                {
                  "user": { "student_id": "${body.studentId}", "real_id": "随机生成一个合法的18位中国身份证号", "name": "${body.name}", "class_name": "高二(3)班", "gender": "${body.gender}", "ethnicity": "汉族或其他", "position": "班长等职务", "enrollment": "2023年9月", "politics": "共青团员", "avatar": "https://api.dicebear.com/7.x/notionists/svg?seed=${Math.random().toString(36).substring(7)}" },
                  "news": [ { "tag": "⭐ 头条新闻", "title": "具有校园特色的新闻标题", "desc": "新闻简短描述", "date": "2024-03-15", "circle_color_1": "bg-accentRed", "circle_color_2": "bg-accentYellow" } ],
                  "archives": {
                    "academic": [ { "title": "高二年级期中考试", "date": "2024.01", "tag": "期中", "totalScore": 620, "totalMax": 750, "gradeRank": 5, "subjects": [ { "name": "语文", "score": 115, "avg": 105, "change": "↑ 2", "changeColor": "text-accentRed" } ]} ],
                    "health": [ { "title": "秋季体质健康测试", "date": "2023.11", "result_summary": "身体各项指标良好。", "details": [ { "item": "身高 (cm)", "value": "175.5", "status": "正常", "color": "text-accentGreen" } ]} ],
                    "library": [],
                    "award": [ { "type": "Honor", "item": "省级三好学生", "date": "2023.12", "issuer": "省教育厅", "description": "品学兼优。" } ]
                  }
                }`;
            } else {
                return new Response('Not Found', { status: 404, headers: corsHeaders });
            }

            // 3. 调用真实的 DeepSeek API
            const response = await fetch('https://api.deepseek.com/chat/completions', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${apiKey}`
                },
                body: JSON.stringify({
                    model: 'deepseek-chat',
                    messages: [
                        { role: 'system', content: 'You are a data API. You must return ONLY valid JSON.' },
                        { role: 'user', content: prompt }
                    ],
                    response_format: { type: "json_object" }
                })
            });

            if (!response.ok) throw new Error("DeepSeek API 请求失败");
            
            const jsonResponse = await response.json();
            let contentText = jsonResponse.choices[0].message.content.trim();
            
            // 清理多余的 markdown 符号
            if (contentText.startsWith("```json")) {
                contentText = contentText.replace(/^```json\n?/, '').replace(/\n?```$/, '');
            }

            // 4. 将解析好的数据安全返回给前端
            return new Response(contentText, {
                status: 200,
                headers: { ...corsHeaders, 'Content-Type': 'application/json' }
            });

        } catch (err) {
            return new Response(JSON.stringify({ error: err.message }), {
                status: 500,
                headers: { ...corsHeaders, 'Content-Type': 'application/json' }
            });
        }
    }
};