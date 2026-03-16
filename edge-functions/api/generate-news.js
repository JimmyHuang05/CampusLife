// 文件路径: ./edge-functions/api/generate-news.js (建议在项目中重命名此文件)
// 访问路径: yourdomain.com/api/generate-news

const corsHeaders = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
};

export default async function onRequest(context) {
    const { request, env } = context;

    // 处理 CORS 跨域预检
    if (request.method === 'OPTIONS') {
        return new Response(null, { headers: corsHeaders });
    }

    if (request.method !== 'POST') {
        return new Response('Method Not Allowed', { status: 405, headers: corsHeaders });
    }

    try {
        const body = await request.json();
        const apiKey = env.DEEPSEEK_API_KEY;

        if (!apiKey) {
            return new Response(JSON.stringify({ error: "EdgeOne 环境变量 DEEPSEEK_API_KEY 未配置" }), { 
                status: 500, 
                headers: { ...corsHeaders, 'Content-Type': 'application/json' } 
            });
        }

        // 允许前端传入特定主题，如果没有则默认生成校园日常新闻
        const topic = body.topic || "校园日常动态";

        const prompt = `你是一个校园新闻编辑AI。请围绕主题"${topic}"生成一条具有校园特色的新闻。必须严格返回一个合法的 JSON 对象，不要包含任何 markdown 代码块符号或多余的说明文字。
        返回格式必须精确如下：
        {
            "tag": "⭐ 标签(例如：头条新闻、校园活动、学术前沿等)",
            "title": "新闻标题(吸引人，符合校园语境)",
            "desc": "新闻简短描述(50字以内，概括核心内容)",
            "date": "YYYY-MM-DD",
            "circle_color_1": "bg-accentRed (从 bg-accentRed, bg-accentBlue, bg-accentGreen, bg-accentYellow 中随机选一个)",
            "circle_color_2": "bg-accentYellow (从上述颜色中再选一个不同的)"
        }`;

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
        
        // 清理 AI 可能返回的 markdown 符号
        if (contentText.startsWith("```json")) {
            contentText = contentText.replace(/^```json\n?/, '').replace(/\n?```$/, '');
        }

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