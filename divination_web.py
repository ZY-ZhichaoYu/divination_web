#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
神秘占卜馆 Web版 v1.0
基于 Streamlit 的网页版占卜应用（单文件，无需其他依赖）
"""

import random
import hashlib
from datetime import datetime, date
import streamlit as st

# ══════════════════════════════════════════════════════════════════════════════
#  工具函数
# ══════════════════════════════════════════════════════════════════════════════
def seeded_rng(seed_str: str) -> random.Random:
    h = int(hashlib.md5(seed_str.encode()).hexdigest(), 16)
    return random.Random(h)

# ══════════════════════════════════════════════════════════════════════════════
#  塔罗牌数据
# ══════════════════════════════════════════════════════════════════════════════
MAJOR_ARCANA = [
    {"id":0,"zh":"愚者","en":"The Fool","roman":"0","sym":"🃏","planet":"天王星","elem":"风",
     "up_kw":["新开始","冒险","纯真","潜力"],"rev_kw":["鲁莽","恐惧","冒失","逃避"],
     "up":"宇宙正在邀请你踏上一段崭新的旅程。放下过去的包袱，以孩童般的好奇心迎接未知——命运之门已经为你悄然开启。相信直觉，勇敢迈出那一步，前方的风景将远超你的想象。",
     "rev":"你可能被恐惧所困，裹足不前；或者正在莽撞行事，不计后果。此刻最需要的，是停下来，深呼吸，诚实地审视自己真正的动机。",
     "adv":"信任宇宙的安排，以开放的心迎接每一种可能性。","lucky":0},
    {"id":1,"zh":"魔术师","en":"The Magician","roman":"I","sym":"🧙‍♂️","planet":"水星","elem":"风",
     "up_kw":["意志力","技巧","创造","行动"],"rev_kw":["欺骗","才能浪费","意志薄弱"],
     "up":"你拥有实现目标所需的一切工具与资源，此刻就握在手中。这是将想法付诸行动的黄金时机——你的意志力就是这个世界上最强大的魔法。整合技能、知识与热情，一切皆有可能。",
     "rev":"才能在被浪费，或者有人正在欺骗你——也许那个人正是你自己。重新审视你的意图，确保你走在诚实的道路上。",
     "adv":"整合所有资源，集中意志，将梦想变为现实。","lucky":1},
    {"id":2,"zh":"女祭司","en":"The High Priestess","roman":"II","sym":"🌙","planet":"月亮","elem":"水",
     "up_kw":["直觉","神秘","潜意识","内在智慧"],"rev_kw":["秘密","压抑感受","与内心脱节"],
     "up":"内在的声音正在向你低语。此刻，向内探索比向外追求更为重要。你的直觉已经知道答案，只需静下心来聆听那份深藏的智慧。不要急于揭晓谜底，时机成熟时一切自会显现。",
     "rev":"你正在忽略内心的声音，或者有重要的事情被隐藏着。这是一个警示：停止压抑你的感受，开始诚实地面对自己的内心世界。",
     "adv":"在沉默中寻找答案，你的直觉比你想象的更可靠。","lucky":2},
    {"id":3,"zh":"女皇","en":"The Empress","roman":"III","sym":"🌿","planet":"金星","elem":"土",
     "up_kw":["丰盛","创造力","滋养","美丽"],"rev_kw":["依赖","创造受阻","匮乏感"],
     "up":"丰盛与创造力如春风般涌入你的生命。这是播种、成长与孕育的时节——无论是事业、关系还是艺术创作，都将在你的精心呵护下开花结果。感受大地母亲的能量，允许自己享受生命的美好。",
     "rev":"创造力受到了阻碍，也许是过度依赖他人，或者内心存在匮乏感。试着重新连接自己与自然，找回那份滋养自己与他人的能力。",
     "adv":"滋养自己，才能滋养他人；当你与自然和谐共处，丰盛自然而至。","lucky":3},
    {"id":4,"zh":"皇帝","en":"The Emperor","roman":"IV","sym":"👑","planet":"火星","elem":"火",
     "up_kw":["权威","稳定","结构","领导力"],"rev_kw":["控制欲","专制","缺乏弹性"],
     "up":"是时候建立秩序，掌控局面了。你拥有足够的智慧和权威来引领前进的方向。在混乱中建立结构，用纪律和坚定的意志打造属于你的稳固基础。责任与权力并行，你已准备好承担这份重量。",
     "rev":"过度控制正在带来问题，或者你在某个权威人物面前感到压迫。找到平衡点——结构是必要的，但僵化只会带来束缚。",
     "adv":"以智慧驾驭权力，以慈悲行使领导。","lucky":4},
    {"id":5,"zh":"教皇","en":"The Hierophant","roman":"V","sym":"⛪","planet":"金星","elem":"土",
     "up_kw":["传统","精神导师","信仰","社会规范"],"rev_kw":["突破传统","叛逆","个人信仰"],
     "up":"向传统智慧寻求指引，或者在某位导师身上找到你需要的答案。遵循既定的道路并非软弱，而是站在前人肩膀上的智慧。信仰、仪式与传统为生命提供了深刻的意义与连接。",
     "rev":"你正在质疑既有的规则与传统——也许是时候开辟自己的道路了。保持尊重，但也允许自己挣脱不再适合你的框架。",
     "adv":"在传统中寻找智慧，在突破中寻找自我。","lucky":5},
    {"id":6,"zh":"恋人","en":"The Lovers","roman":"VI","sym":"💞","planet":"水星","elem":"风",
     "up_kw":["爱情","选择","和谐","价值观对齐"],"rev_kw":["价值观冲突","糟糕的选择","关系失衡"],
     "up":"一个重要的选择正摆在你面前，而这个选择将深深影响你的人生方向。无论是关于爱情还是其他，核心在于：你是否正在做一个真正符合内心价值观的决定？当两颗心真正相通，世界都会为之鸣响。",
     "rev":"关系中存在失衡，或者你正面临一个你其实已经知道答案的艰难选择。诚实地面对那个你一直回避的内心声音。",
     "adv":"真正的爱始于对自己的诚实。","lucky":6},
    {"id":7,"zh":"战车","en":"The Chariot","roman":"VII","sym":"🏆","planet":"月亮","elem":"水",
     "up_kw":["意志","胜利","控制","决心"],"rev_kw":["失控","方向迷失","强行推进"],
     "up":"胜利触手可及！通过坚强的意志和专注的决心，你正在克服重重障碍向前挺进。保持对内心冲突的掌控，将分散的力量整合为一个方向，没有什么能阻止一个意志坚定的人。",
     "rev":"事情正在失控，或者你在强行推进本不该强求的事。暂停一下，重新找回内心的方向感，再出发。",
     "adv":"驾驭自己内心的矛盾，才能真正驾驭外部世界。","lucky":7},
    {"id":8,"zh":"力量","en":"Strength","roman":"VIII","sym":"🦁","planet":"太阳","elem":"火",
     "up_kw":["内在力量","勇气","耐心","慈悲"],"rev_kw":["怀疑自己","软弱","恐惧"],
     "up":"真正的力量不来自蛮力，而来自内心深处的平静与慈悲。你拥有足够的勇气和耐心去面对眼前的挑战。用爱而非恐惧来驯服内心的野性，你会发现自己比以为的更加强大。",
     "rev":"你正在怀疑自己的能力，或者在用错误的方式运用力量。内在的恐惧需要被温柔地面对，而非压制。",
     "adv":"温柔是最强大的力量形式。","lucky":8},
    {"id":9,"zh":"隐士","en":"The Hermit","roman":"IX","sym":"🏔️","planet":"水星","elem":"土",
     "up_kw":["内省","孤独","寻找真相","引导"],"rev_kw":["过度孤立","拒绝帮助","迷失"],
     "up":"现在是向内寻找答案的时刻。退离喧嚣，在独处中与自己的灵魂相遇。你的内在之光足以照亮前方的道路——也许还能成为他人的引领者。深刻的智慧往往在静默中才能听见。",
     "rev":"过度的孤立正在伤害你，或者你在拒绝他人的帮助。适度的独处是滋养，但完全的封闭会让你迷失在自己的黑暗中。",
     "adv":"在独处中找到自己，在与人连接中分享光明。","lucky":9},
    {"id":10,"zh":"命运之轮","en":"Wheel of Fortune","roman":"X","sym":"🎡","planet":"木星","elem":"火",
     "up_kw":["命运","转机","周期","好运"],"rev_kw":["厄运","抗拒改变","周期受阻"],
     "up":"命运的齿轮正在转动，带来积极的变化和新的机遇。好运降临！记住，一切都是周期性的——高潮与低谷交替出现。这次轮转带来的是上升与扩展，抓住这个时机乘势而上。",
     "rev":"厄运似乎在作祟，或者你正在抗拒生命自然的流动。记住：轮子总会再次转动，坏运气终将过去，保持耐心与信心。",
     "adv":"顺应生命的自然节奏，每一次转变都是成长的契机。","lucky":10},
    {"id":11,"zh":"正义","en":"Justice","roman":"XI","sym":"⚖️","planet":"金星","elem":"风",
     "up_kw":["公平","真相","因果","平衡"],"rev_kw":["不公平","逃避责任","失衡"],
     "up":"宇宙的天平正在校准，因果法则在运作。你将得到你所应得的，无论好坏。这张牌呼唤诚实与责任感——对自己的行为负责，以公正的眼光看待自己和他人。",
     "rev":"不公平的情况正在发生，或者你在逃避对自己行为的责任。无法逃避因果，最好的应对方式是坦诚地面对自己的选择。",
     "adv":"诚实对待自己，是获得真正公平的唯一方式。","lucky":11},
    {"id":12,"zh":"倒吊人","en":"The Hanged Man","roman":"XII","sym":"🙃","planet":"海王星","elem":"水",
     "up_kw":["暂停","新视角","牺牲","等待"],"rev_kw":["无谓牺牲","不愿放手","拖延"],
     "up":"生命正在邀请你暂停，从不同的角度看待问题。有时候，放弃控制、甘愿等待，本身就是一种深刻的智慧。也许你需要放下某些执念，才能看到真正的出路。这段暂停期蕴含着重要的启示。",
     "rev":"你在做无谓的牺牲，或者明明该放手却死死抓住不放。区分哪些是真正的智慧等待，哪些只是你在拖延和逃避。",
     "adv":"换个角度，世界将呈现全新的面貌。","lucky":12},
    {"id":13,"zh":"死神","en":"Death","roman":"XIII","sym":"🦋","planet":"冥王星","elem":"水",
     "up_kw":["转变","结束","蜕变","新生"],"rev_kw":["抗拒改变","停滞","无法放手"],
     "up":"不要被这张牌的名字吓到——死神牌代表的是深刻的蜕变与转化。一个阶段正在结束，为新的开始腾出空间。只有让旧的消逝，新的才能诞生。拥抱这份转变，它将带你走向更真实的自我。",
     "rev":"你正在死死抓住已经结束的事物，抗拒不可避免的改变。这种抗拒正在消耗你的能量，让自己停滞不前。",
     "adv":"放手，是为了拥抱更好的未来。","lucky":13},
    {"id":14,"zh":"节制","en":"Temperance","roman":"XIV","sym":"🌊","planet":"木星","elem":"火",
     "up_kw":["平衡","节制","调和","耐心"],"rev_kw":["失衡","过度","不耐烦"],
     "up":"生命需要在对立面之间找到优雅的平衡。不过度也不匮乏，慢慢将不同的元素调和成完美的配比。你的耐心与适度正是此刻最需要的美德。相信这个缓慢但稳定的炼金过程。",
     "rev":"某些方面出现了严重的失衡，或者你正在做过激的事情。停下来，重新找到中间的道路，极端永远不是长久之计。",
     "adv":"在极端之间找到中道，这是真正的智慧。","lucky":14},
    {"id":15,"zh":"恶魔","en":"The Devil","roman":"XV","sym":"⛓️","planet":"土星","elem":"土",
     "up_kw":["束缚","执念","阴影","物质主义"],"rev_kw":["挣脱束缚","自我意识","释放"],
     "up":"你是否感到被某种力量束缚？这张牌揭示了我们生命中的执念、上瘾或不健康的模式。好消息是：那些锁链其实是你可以亲手解开的。第一步是承认它们的存在，直面自己阴暗面的力量。",
     "rev":"你正在从某种束缚中挣脱出来！觉醒已经开始。认识到自己的局限和模式，是走向自由的第一步。继续前进，解放就在眼前。",
     "adv":"直面你的阴影，才能真正从它的掌控中解脱。","lucky":15},
    {"id":16,"zh":"塔","en":"The Tower","roman":"XVI","sym":"⚡","planet":"火星","elem":"火",
     "up_kw":["突变","崩塌","启示","解放"],"rev_kw":["避免灾难","拖延崩塌","内部崩塌"],
     "up":"闪电击中高塔，虚假的结构轰然倒塌——但这往往是解放的开始。眼前的剧变看似破坏，实则是宇宙在清除那些建立在谎言或不稳定基础上的事物。在废墟中，真正属于你的东西将会留下。",
     "rev":"你在拼命阻止一场不可避免的崩塌，或者变化正在从内部缓慢发生。有时候，最好的应对是接受改变，而非消耗一切去维持表面的稳定。",
     "adv":"有些东西崩塌，是为了让真正坚实的东西显现。","lucky":16},
    {"id":17,"zh":"星星","en":"The Star","roman":"XVII","sym":"⭐","planet":"天王星","elem":"风",
     "up_kw":["希望","治愈","灵感","更新"],"rev_kw":["失去希望","绝望","断开连接"],
     "up":"在最黑暗的夜空中，星星依然闪烁。这是一张充满希望与治愈能量的牌——经历了风雨之后，平静与宁静正在降临。你与宇宙的能量深深相连，被无条件地支持着。相信美好的事物正在向你流动而来。",
     "rev":"你正在失去希望，感到与宇宙能量断开了连接。这种感受是真实的，但它不是永久的。在绝望中，记得抬头看看那些依然闪烁的星星。",
     "adv":"即使看不见光明，也要相信它的存在。","lucky":17},
    {"id":18,"zh":"月亮","en":"The Moon","roman":"XVIII","sym":"🌕","planet":"月亮","elem":"水",
     "up_kw":["幻象","潜意识","恐惧","直觉"],"rev_kw":["真相浮现","恐惧消散","清晰度"],
     "up":"月光下，幻象与现实交织，梦境与清醒模糊了边界。你的潜意识正在发送强烈的信号——注意你的梦境和直觉，它们在告诉你一些白天无法看清的真相。小心被表象迷惑，真相比你看到的更复杂。",
     "rev":"迷雾正在散去，被隐藏的真相即将浮现。那些曾经困扰你的恐惧和幻象正在失去力量。清晰即将到来，准备好以更清醒的眼光看待一切。",
     "adv":"在朦胧中保持直觉的清醒，而非理性的掌控。","lucky":18},
    {"id":19,"zh":"太阳","en":"The Sun","roman":"XIX","sym":"☀️","planet":"太阳","elem":"火",
     "up_kw":["喜悦","活力","成功","真实自我"],"rev_kw":["过度乐观","暂时阴云","内在阳光"],
     "up":"这是整副塔罗中最明亮、最充满正能量的牌之一！喜悦、成功与活力正在向你涌来。你的真实自我在阳光下自由绽放，一切都充满了可能性与热情。享受这段美好的时光，让自己的光芒照耀世界。",
     "rev":"阳光暂时被乌云遮蔽，但它从未消失。你也许过度乐观，或者在努力维持表面的快乐。记住：即使感受不到，你内在的阳光依然存在。",
     "adv":"允许自己快乐——你值得被阳光照耀。","lucky":19},
    {"id":20,"zh":"审判","en":"Judgement","roman":"XX","sym":"📯","planet":"冥王星","elem":"火",
     "up_kw":["觉醒","救赎","内心呼唤","重生"],"rev_kw":["自我怀疑","拒绝觉醒","错失呼唤"],
     "up":"生命中一个深刻的觉醒时刻已经到来。那个一直在内心深处呼唤你的声音——现在是时候回应它了。这不是审判，而是救赎；不是结束，而是以全新的自我重生。你准备好回应那个最高的召唤了吗？",
     "rev":"你正在忽略内心深处的呼唤，或者被自我怀疑所困。也许你在评判自己太过严苛，导致无法接受改变和成长的机会。",
     "adv":"听从内心最深处的那声呼唤，那是你真实命运的方向。","lucky":20},
    {"id":21,"zh":"世界","en":"The World","roman":"XXI","sym":"🌍","planet":"土星","elem":"土",
     "up_kw":["完成","整合","成就","圆满"],"rev_kw":["未竟之事","短暂的捷径","停滞"],
     "up":"恭喜！你已经到达了一个重要旅程的终点，一个美丽的循环正在圆满完成。这是全力以赴后的成就感，是内外统一的圆满境界。庆祝你的到达，同时也准备好，一个全新的旅程即将从这里展开。",
     "rev":"有些事情还没有真正完成——也许你在走捷径，或者有重要的功课尚未学会。完整的圆满需要真正地经历和整合每一个阶段，不要急于宣告结束。",
     "adv":"真正的圆满不是终点，而是新的开始的最佳准备。","lucky":21},
]

# ══════════════════════════════════════════════════════════════════════════════
#  星座数据
# ══════════════════════════════════════════════════════════════════════════════
ZODIAC = [
    {"name":"白羊座","en":"Aries","sym":"♈","dates":"3/21–4/19","elem":"火","ruler":"火星","trait":"勇敢、热情、冲动、领导力强"},
    {"name":"金牛座","en":"Taurus","sym":"♉","dates":"4/20–5/20","elem":"土","ruler":"金星","trait":"稳重、耐心、固执、热爱美食"},
    {"name":"双子座","en":"Gemini","sym":"♊","dates":"5/21–6/20","elem":"风","ruler":"水星","trait":"机智、善变、好奇、沟通高手"},
    {"name":"巨蟹座","en":"Cancer","sym":"♋","dates":"6/21–7/22","elem":"水","ruler":"月亮","trait":"情感丰富、顾家、敏感、保护欲强"},
    {"name":"狮子座","en":"Leo","sym":"♌","dates":"7/23–8/22","elem":"火","ruler":"太阳","trait":"自信、慷慨、戏剧化、渴望认可"},
    {"name":"处女座","en":"Virgo","sym":"♍","dates":"8/23–9/22","elem":"土","ruler":"水星","trait":"细心、完美主义、分析力强、服务精神"},
    {"name":"天秤座","en":"Libra","sym":"♎","dates":"9/23–10/22","elem":"风","ruler":"金星","trait":"追求平衡、外交手腕、美感、优柔寡断"},
    {"name":"天蝎座","en":"Scorpio","sym":"♏","dates":"10/23–11/21","elem":"水","ruler":"冥王星","trait":"深刻、神秘、占有欲强、洞察力惊人"},
    {"name":"射手座","en":"Sagittarius","sym":"♐","dates":"11/22–12/21","elem":"火","ruler":"木星","trait":"自由奔放、乐观、哲学思维、不拘一格"},
    {"name":"摩羯座","en":"Capricorn","sym":"♑","dates":"12/22–1/19","elem":"土","ruler":"土星","trait":"务实、雄心勃勃、自律、传统价值观"},
    {"name":"水瓶座","en":"Aquarius","sym":"♒","dates":"1/20–2/18","elem":"风","ruler":"天王星","trait":"革新、独立、人道主义、特立独行"},
    {"name":"双鱼座","en":"Pisces","sym":"♓","dates":"2/19–3/20","elem":"水","ruler":"海王星","trait":"敏感、富有同理心、梦幻、艺术天赋"},
]

ZODIAC_TEMPLATES = {
    "general": [
        "今日宇宙能量流动顺畅，你的直觉异常敏锐。适合做出重要决策，但记得在行动前深思熟虑。",
        "今天是整合与反思的好时机。放慢脚步，观察周围的细节，你会发现一些平时忽略的重要信息。",
        "强烈的能量推动你向前冲，但也要注意不要在急进中错过重要细节。保持热情的同时，留意身边人的感受。",
        "今天适合与信任的人深度交流。一段对话可能带来意想不到的启示，为你的某个困惑提供全新的视角。",
        "宇宙正在为你准备一个惊喜。保持开放的心态，不要把计划安排得太满，给意外的美好留点空间。",
        "内在的清晰度今天特别高。那些困扰你许久的问题，也许在今天早晨的第一杯茶里就能找到答案。",
    ],
    "love": [
        "感情运势平稳向上。单身者可能在意想不到的地方遇见一个有趣的灵魂；有伴侣者，今天适合进行一次深入的心灵对话。",
        "爱情需要主动灌溉。不要等待对方先表达——你率先付出的那一份温柔，将收获加倍的回应。",
        "感情方面有些小摩擦，但请记得：冲突是加深了解的机会。保持耐心和善意，问题终将化解。",
        "今天你的魅力值拉满！你散发着一种神秘而迷人的气质，周围的人都会不由自主地被你吸引。",
        "旧情人或旧缘分可能重新出现在生活中。无论以何种形式，这次重逢都蕴含着需要被完成的功课。",
        "感情中最重要的事是诚实。今天，勇敢说出那句你一直藏在心里的话——真相让关系更坚固，而非相反。",
    ],
    "career": [
        "工作上有新的机遇浮现，但竞争也同样激烈。展示你独特的视角和解决方案，这将是你脱颖而出的关键。",
        "今天适合处理积压的事务，逐一清空你的待办清单。完成率将为你带来满足感和向前冲的动力。",
        "一个意想不到的合作机会可能出现。不要因为对方的背景与你不同就拒绝，多元化的合作往往能带来突破。",
        "财运上有正面信号！留意那些看似微小的投资或学习机会，它们在未来可能带来丰厚的回报。",
        "工作效率极高的一天。把最重要、最有挑战性的任务放在今天处理，你会发现自己的执行力出乎意料地强。",
        "适度休息也是高效工作的一部分。今天可以刻意放慢节奏，用以策划未来的方向，而非一味地埋头苦干。",
    ],
    "health": [
        "身体状态良好，但要注意适度。今天容易因为亢奋而过度消耗，记得在忙碌中为自己安排充足的休息时间。",
        "精神能量充沛！这是开始一项新的运动习惯的好日子，哪怕只是每天散步20分钟，坚持就是胜利。",
        "情绪健康需要关注。你积压了一些未被处理的感受，找一个安全的方式表达它们——写日记、绘画或运动都是好选择。",
        "身心都在呼唤一次真正的放松。今晚早些上床，远离电子屏幕，让深度睡眠为明天充电。",
        "今天适合进行冥想或瑜伽等放松练习。短短15分钟的正念冥想，可以为你带来一整天的平静与专注。",
        "注意饮食，不要因为压力大就用美食填补情绪空洞。真正的滋养来自内心，而食物只是支撑，不是解药。",
    ],
}

# ══════════════════════════════════════════════════════════════════════════════
#  周易数据
# ══════════════════════════════════════════════════════════════════════════════
TRIGRAMS = {
    0b000: ("坤","☷","地","柔顺、承载、阴性能量"),
    0b001: ("震","☳","雷","行动、震动、新开始"),
    0b010: ("坎","☵","水","危险、流动、智慧"),
    0b011: ("兑","☱","泽","喜悦、表达、交流"),
    0b100: ("艮","☶","山","静止、等待、沉思"),
    0b101: ("离","☲","火","光明、依附、洞察"),
    0b110: ("巽","☴","风","渗透、谦逊、顺从"),
    0b111: ("乾","☰","天","强健、创造、阳性能量"),
}

HEXAGRAM_NAMES = {
    (0b111,0b111):("乾","天天乾","自强不息，厚德载物"),
    (0b000,0b000):("坤","地地坤","厚德载物，顺势而为"),
    (0b001,0b010):("屯","水雷屯","万事开头难，坚持初心"),
    (0b010,0b100):("蒙","山水蒙","蒙昧启智，求教于贤"),
    (0b111,0b010):("需","水天需","等待时机，养精蓄锐"),
    (0b010,0b111):("讼","天水讼","争讼宜止，和解为上"),
    (0b000,0b010):("师","地水师","以柔克刚，守正出奇"),
    (0b010,0b000):("比","水地比","亲比团结，上下相应"),
    (0b111,0b110):("小畜","风天小畜","积累小成，循序渐进"),
    (0b110,0b111):("履","天风履","小心谨慎，履险如夷"),
    (0b000,0b111):("泰","地天泰","天地交泰，万物通顺"),
    (0b111,0b000):("否","天地否","闭塞不通，静待时变"),
    (0b101,0b111):("同人","天火同人","与人和谐，志同道合"),
    (0b111,0b101):("大有","火天大有","大丰收，光明在上"),
    (0b000,0b100):("谦","地山谦","谦虚谨慎，自我约束"),
    (0b001,0b000):("豫","雷地豫","愉悦顺从，不可过度"),
    (0b011,0b001):("随","泽雷随","随势而动，灵活应变"),
    (0b110,0b100):("蛊","山风蛊","整治积弊，除旧布新"),
    (0b000,0b110):("临","地风临","临近成功，保持谦逊"),
    (0b110,0b000):("观","风地观","观察审视，以知进退"),
    (0b101,0b001):("噬嗑","火雷噬嗑","冲破阻碍，刚柔并济"),
    (0b001,0b101):("贲","山火贲","文饰外表，内外兼修"),
    (0b111,0b001):("无妄","天雷无妄","顺应自然，无为而治"),
    (0b100,0b111):("大畜","山天大畜","积蓄力量，蓄势待发"),
    (0b100,0b001):("颐","山雷颐","养正节食，修身养性"),
    (0b011,0b110):("大过","泽风大过","力量超载，寻求平衡"),
    (0b010,0b010):("坎","水水坎","险中求安，坚守正道"),
    (0b101,0b101):("离","火火离","光明双叠，坚持正念"),
    (0b011,0b100):("咸","泽山咸","感应共鸣，心有灵犀"),
    (0b001,0b110):("恒","雷风恒","坚持恒久，持之以恒"),
    (0b111,0b100):("遁","天山遁","适时退隐，以待东山"),
    (0b001,0b111):("大壮","雷天大壮","阳刚强盛，戒骄戒躁"),
    (0b101,0b000):("晋","火地晋","前进上升，日新月异"),
    (0b000,0b101):("明夷","地火明夷","光明受阻，韬光养晦"),
    (0b101,0b110):("家人","风火家人","家道和谐，内外一致"),
    (0b110,0b101):("睽","火泽睽","对立中求统一，异中求同"),
    (0b010,0b100):("蹇","水山蹇","艰难险阻，求援于贤"),
    (0b001,0b010):("解","雷水解","解除困难，重获自由"),
    (0b100,0b011):("损","山泽损","减损自我，奉献他人"),
    (0b110,0b001):("益","风雷益","增益扩展，与人分享"),
    (0b111,0b011):("夬","泽天夬","果断决断，除去邪恶"),
    (0b000,0b011):("萃","泽地萃","聚集团结，凝聚力量"),
    (0b010,0b110):("井","水风井","取之不尽，养民利民"),
    (0b011,0b101):("革","泽火革","改革变革，除旧迎新"),
    (0b101,0b011):("鼎","火泽鼎","炼化升华，成就大业"),
    (0b001,0b001):("震","雷雷震","警醒振奋，以畏求吉"),
    (0b100,0b100):("艮","山山艮","静止思考，知止而后安"),
    (0b001,0b110):("渐","风山渐","循序渐进，稳扎稳打"),
    (0b001,0b101):("丰","雷火丰","丰盛繁荣，明智行动"),
    (0b101,0b100):("旅","火山旅","旅途奔波，保持谨慎"),
    (0b110,0b110):("巽","风风巽","柔顺渗透，谦虚致远"),
    (0b011,0b011):("兑","泽泽兑","喜悦满溢，与人同乐"),
    (0b110,0b010):("节","水泽节","节制适度，守正中庸"),
    (0b001,0b100):("小过","雷山小过","小有过失，谨慎修正"),
    (0b010,0b101):("既济","水火既济","大功告成，居安思危"),
    (0b101,0b010):("未济","火水未济","尚未完成，继续努力"),
}

# ══════════════════════════════════════════════════════════════════════════════
#  数字命理数据
# ══════════════════════════════════════════════════════════════════════════════
NUMEROLOGY = {
    1:  {"title":"独立领袖 — 1号生命之路","symbol":"🌟",
         "trait":"你天生具有领导力和开创精神。独立、自主、充满个人魅力是你的核心特质。你来到这个世界是为了开创新路，而非追随他人的脚步。",
         "mission":"学会在独立与接受帮助之间找到平衡。真正的领袖不是孤军奋战，而是知道何时带领，何时借助集体的智慧。",
         "challenge":"孤独感与过度自我依赖。学会接受他人的支持，不是软弱，而是智慧。",
         "lucky_color":"金色与深红","lucky_stone":"红宝石、石榴石"},
    2:  {"title":"和谐使者 — 2号生命之路","symbol":"🕊️",
         "trait":"你是天生的外交官，拥有深刻的同理心和合作精神。你在群体中如鱼得水，能感知到他人微妙的情绪变化，总是在维持和谐与平衡。",
         "mission":"学会在付出与自我保护之间找到平衡。你的温柔是礼物，但也需要为自己设立健康的边界。",
         "challenge":"过于在意他人评价，有时会牺牲自己的需求。",
         "lucky_color":"银色与淡蓝","lucky_stone":"月光石、蓝托帕石"},
    3:  {"title":"创意表达者 — 3号生命之路","symbol":"🎨",
         "trait":"你充满创造力、乐观积极，有着感染人心的表达天赋。无论是艺术、写作还是演讲，你都能用独特的方式传递情感和想法。",
         "mission":"将你的创意天赋付诸实践，不只停留在想象中。通过表达自我，你能为这个世界带来独特的光彩。",
         "challenge":"注意力分散，难以专注完成一件事。深度比广度更能展现你真正的才华。",
         "lucky_color":"紫色与金黄","lucky_stone":"紫水晶、黄水晶"},
    4:  {"title":"稳固建造者 — 4号生命之路","symbol":"🏛️",
         "trait":"你是实际可靠、勤奋耐心的建造者。你相信一步一个脚印，用双手和智慧创造稳固而持久的成果。责任感和诚信是你最宝贵的品质。",
         "mission":"在稳定与灵活之间找到平衡。你擅长建造，但也要学会在既定框架外思考，因为有些时候，旧有的结构需要被突破。",
         "challenge":"过于固执，难以接受改变。开放性是你需要培养的能力。",
         "lucky_color":"墨绿与深棕","lucky_stone":"翡翠、黑曜石"},
    5:  {"title":"自由探险家 — 5号生命之路","symbol":"🌍",
         "trait":"你生来渴望自由、变化和冒险。你的好奇心无边无际，对生活充满热情，能在任何环境中快速适应并找到乐趣。",
         "mission":"学会在自由与责任之间取得平衡。真正的自由不是逃离，而是在承担责任的前提下依然保持内心的飞翔。",
         "challenge":"注意力容易分散，有时难以坚持完成。",
         "lucky_color":"橙色与天蓝","lucky_stone":"海蓝宝石、橙色方解石"},
    6:  {"title":"滋养守护者 — 6号生命之路","symbol":"🌻",
         "trait":"你有着天生的责任感和对家庭、社区的深深关怀。你是天然的治愈者和照顾者，以温暖和爱意滋养着周围的一切。",
         "mission":"在付出的同时，也要学会接受照顾。你照顾他人的能力是礼物，但别忘了也给自己同样的温柔。",
         "challenge":"完美主义倾向可能让你对自己和他人过于苛刻。",
         "lucky_color":"玫瑰粉与草绿","lucky_stone":"粉晶、翡翠"},
    7:  {"title":"神秘智者 — 7号生命之路","symbol":"🔭",
         "trait":"你天生具有深刻的分析能力和对真理的渴望。你倾向于独处和沉思，喜欢挖掘事物的本质，是一位深刻的思想者和灵性探索者。",
         "mission":"将你的内在智慧与外部世界分享。智慧不是用来独自珍藏的，而是要在适当的时机传递给需要的人。",
         "challenge":"孤立自我，有时难以建立深入的情感连接。",
         "lucky_color":"深紫与藏青","lucky_stone":"紫水晶、蓝玉髓"},
    8:  {"title":"权力成就者 — 8号生命之路","symbol":"♾️",
         "trait":"你天生具有商业头脑和对成功的强烈驱动力。你有能力积累财富、权力和影响力，并将其用于创造实质性的成果。",
         "mission":"学会用权力服务他人，而非只是积累个人成就。真正的成功是物质与精神、个人与集体的同步丰盛。",
         "challenge":"对失败的恐惧，以及对权力和控制的过度追求。",
         "lucky_color":"黑金与深红","lucky_stone":"黑曜石、红宝石"},
    9:  {"title":"人道主义者 — 9号生命之路","symbol":"🌈",
         "trait":"你是这个数字中最具普世关怀的灵魂。你有着超越个人、服务全人类的愿望，同理心和慈悲心是你最核心的品质。",
         "mission":"学会在给予中不失去自我。你对世界的爱是真实的，但你也是这个世界的一部分，也同样值得被爱。",
         "challenge":"理想主义可能导致失望；放手与结束对你来说特别困难。",
         "lucky_color":"金色与彩虹色","lucky_stone":"彩色宝石、拉长石"},
    11: {"title":"灵性使者 — 11号主数字","symbol":"✨",
         "trait":"11是主数字，代表灵性觉醒与直觉的巅峰。你是灵感的管道，能感受到普通人无法感知的精微能量，天生具有灵性天赋与洞察力。",
         "mission":"将你超凡的直觉转化为对他人有实际帮助的智慧和启示。你的存在本身就是一束光。",
         "challenge":"能量极为敏感，容易受环境影响；需要大量独处时间来充电。",
         "lucky_color":"银白与深紫","lucky_stone":"月光石、紫水晶"},
    22: {"title":"宏大建造师 — 22号主数字","symbol":"🏗️",
         "trait":"22是最强大的主数字，代表将宏大梦想转化为现实的能力。你天生具有建造宏大事业的潜力，能将灵性智慧落实到物质世界中。",
         "mission":"用你的实践能力和远见，为世界建造持久而有意义的事物。",
         "challenge":"压力巨大，容易因高自我期望而不堪重负。",
         "lucky_color":"黑金与深绿","lucky_stone":"黑碧玺、绿幽灵"},
    33: {"title":"大爱导师 — 33号主数字","symbol":"❤️‍🔥",
         "trait":"33是最高振动的主数字，代表无条件的爱与大智慧。你天生是他人的治愈者与导师，以慈悲和爱的振动影响着周围所有人。",
         "mission":"成为爱的活生生的体现，用言行教导他人什么是无条件的慈悲。",
         "challenge":"容易背负他人的痛苦；必须学会健康的能量边界。",
         "lucky_color":"金色与玫瑰红","lucky_stone":"粉晶、黄金矿石"},
}

# ══════════════════════════════════════════════════════════════════════════════
#  每日一签数据
# ══════════════════════════════════════════════════════════════════════════════
FORTUNE_SLIPS = [
    {"grade":"上上签","num":1,"title":"飞龙在天","poem":"鸿鹄展翅九万里，扶摇直上凌云端。","general":"诸事大吉，运势如日中天，所谋皆遂心愿。","love":"情投意合，缘分天定，美好姻缘水到渠成。","career":"贵人相助，事业腾飞，把握良机大展宏图。","health":"精力充沛，身体康泰，保持现有生活方式。"},
    {"grade":"上签","num":2,"title":"春风化雨","poem":"随风潜入夜，润物细无声，好雨知时节。","general":"吉祥顺遂，如春风化雨，万事渐入佳境。","love":"感情升温，细水长流，真心终得真情回应。","career":"稳步积累，贵人提携，功到自然成。","health":"气血调和，注意休息，身心逐渐复苏。"},
    {"grade":"上签","num":3,"title":"金榜题名","poem":"十年寒窗无人问，一举成名天下知。","general":"付出终有回报，努力将迎来丰厚收获。","love":"缘分在努力中成熟，主动表达情感。","career":"晋升有望，才华得到认可，把握展示机会。","health":"身体状况良好，保持锻炼习惯。"},
    {"grade":"中上签","num":4,"title":"柳暗花明","poem":"山重水复疑无路，柳暗花明又一村。","general":"困境已过，转机将至，保持耐心迎接曙光。","love":"感情经历考验，风雨过后见彩虹。","career":"瓶颈期将突破，坚持方向不动摇。","health":"慢性问题逐步改善，配合调理事半功倍。"},
    {"grade":"中上签","num":5,"title":"顺水行舟","poem":"乘风破浪会有时，直挂云帆济沧海。","general":"顺势而为，借力打力，事半功倍。","love":"感情顺畅，珍惜眼前，共同迎接美好未来。","career":"机会来临，顺势而上，不可迟疑。","health":"气运通畅，适当增加运动量。"},
    {"grade":"中签","num":6,"title":"守株待兔","poem":"行到水穷处，坐看云起时。","general":"时机未到，宜守不宜攻，静观其变。","love":"感情需要耐心培育，急于求成适得其反。","career":"当下宜积累沉淀，待时机成熟再出击。","health":"注意劳逸结合，避免透支精力。"},
    {"grade":"中签","num":7,"title":"云开见日","poem":"不经一番寒彻骨，哪得梅花扑鼻香。","general":"历经磨砺方能成就，当前困难是成长的必要。","love":"感情需要经营，多一分付出多一分收获。","career":"历练中成长，困难正在锤炼你的能力。","health":"有些小毛病需要认真对待，不可忽视。"},
    {"grade":"中签","num":8,"title":"平步青云","poem":"不积跬步，无以至千里；不积小流，无以成江海。","general":"积累是关键，点滴努力终成大器。","love":"感情需要日积月累的陪伴与理解。","career":"踏实积累比急功近利更能走远。","health":"规律生活是健康的基础，坚持好习惯。"},
    {"grade":"中签","num":9,"title":"阴晴不定","poem":"世事无常云变幻，随遇而安是智慧。","general":"运势起伏，保持平常心，不以物喜不以己悲。","love":"感情有些波动，多沟通少误会。","career":"情况变化较快，灵活应对是关键。","health":"情绪影响健康，保持心情平稳。"},
    {"grade":"中下签","num":10,"title":"逆水行舟","poem":"行路难，行路难，多歧路，今安在。","general":"当前阻力较大，需要加倍努力方能前进。","love":"感情遭遇阻碍，需要更多耐心与包容。","career":"遇到挑战，不可退缩，逆境是磨砺。","health":"身体需要关注，及时休养调整。"},
    {"grade":"中下签","num":11,"title":"困龙得水","poem":"潜龙勿用，待时而动；厚积薄发，终见天日。","general":"处于蛰伏期，当下不宜大动，积蓄力量。","love":"感情暂时受阻，保持信念静待缘分。","career":"低调蓄力，不宜冒进，等待时机。","health":"注意休息，让身体恢复元气。"},
    {"grade":"下签","num":12,"title":"风雨如晦","poem":"风雨如晦，鸡鸣不已；既见君子，云胡不喜。","general":"困难时期，坚守本心，黑暗后必迎黎明。","love":"感情遇到考验，真心可化解误解。","career":"艰难时期需要坚持，不可轻言放弃。","health":"身体需要重视，及时就医调理。"},
    {"grade":"上上签","num":13,"title":"鱼跃龙门","poem":"黄河之水天上来，一鱼化龙冲天际。","general":"大运来临，一跃而上，命运翻转在此一时。","love":"桃花运旺盛，姻缘天定，有情人终成眷属。","career":"重大突破在即，全力以赴把握机遇。","health":"生命力旺盛，气场强大，精力充沛。"},
    {"grade":"上签","num":14,"title":"吉星高照","poem":"福星临门百事兴，吉祥如意满乾坤。","general":"福运当头，诸事顺利，吉星相护。","love":"有望遇见真命天子/天女，缘分近了。","career":"项目推进顺利，上级赏识，前途光明。","health":"体力充沛，精神饱满，免疫力强。"},
    {"grade":"中上签","num":15,"title":"拨云见日","poem":"拨云睹青天，破浪见沧海。","general":"迷雾渐散，真相即将大白，坚持判断。","love":"误会即将消除，感情重回正轨。","career":"困惑即将解开，方向越来越清晰。","health":"困扰已久的问题，治疗方向即将明朗。"},
    {"grade":"中签","num":16,"title":"随缘自在","poem":"菩提本无树，明镜亦非台；本来无一物，何处惹尘埃。","general":"放下执念，随缘而行，自在是最好的状态。","love":"不强求，顺其自然，缘来则聚缘去则散。","career":"不执着于结果，专注过程，结果自然来。","health":"心平气和是良药，保持内心平静。"},
    {"grade":"中上签","num":17,"title":"厚积薄发","poem":"千淘万漉虽辛苦，吹尽狂沙始到金。","general":"积累到临界点，爆发时刻即将来临。","love":"情感在时间的沉淀中愈发浓郁。","career":"多年努力即将开花结果，坚持到底。","health":"调养到位，康复可期，坚持疗程。"},
    {"grade":"中签","num":18,"title":"持之以恒","poem":"为山九仞，功亏一篑；持之以恒，方得始终。","general":"切忌功亏一篑，坚持到最后一步。","love":"感情不可三心二意，专一才能长久。","career":"现在放弃太可惜，距成功只差最后一步。","health":"调理不可半途而废，坚持才有效果。"},
    {"grade":"上签","num":19,"title":"否极泰来","poem":"穷则变，变则通，通则久；物极必反，剥极而复。","general":"最坏的时候已经过去，好运正在回头。","love":"低谷期结束，感情重新焕发生机。","career":"困境即将反转，新机遇即将出现。","health":"身体正在好转，调理进入正循环。"},
    {"grade":"中上签","num":20,"title":"心想事成","poem":"诚心所至，金石为开；志之所趋，无远弗届。","general":"心诚则灵，你的心愿正在被宇宙聆听。","love":"真心付出必有真情回报，相信爱情。","career":"明确目标，全力以赴，心想事成不是梦。","health":"积极的心态加速康复，正向思维是良药。"},
    {"grade":"中下签","num":21,"title":"关关难过","poem":"天将降大任于斯人也，必先苦其心志。","general":"考验接连而来，但每一关都是成长的台阶。","love":"感情面临多重考验，需要坚定信念。","career":"阻碍较多，但克服每一个困难后你会更强。","health":"身体发出警示信号，认真对待健康。"},
    {"grade":"中签","num":22,"title":"万事俱备","poem":"东风不与周郎便，铜雀春深锁二乔。","general":"准备充分，只欠东风，等待时机成熟。","love":"条件已经成熟，就差那一步勇气。","career":"万事俱备，抓住下一个出现的机会。","health":"身体状况稳定，维持现有的保养方案。"},
    {"grade":"上上签","num":23,"title":"百年好合","poem":"在天愿作比翼鸟，在地愿为连理枝。","general":"贵人相聚，喜事连连，百年好合的吉兆。","love":"姻缘极佳，若有意中人，此时表白大吉。","career":"合作项目大吉，团队合力共创佳绩。","health":"身心和谐，内外平衡，状态极佳。"},
    {"grade":"中上签","num":24,"title":"龙凤呈祥","poem":"龙游浅水遭虾戏，虎落平阳被犬欺；得志猫儿雄于虎，落魄凤凰不如鸡。","general":"运势上升，展示才华的时机已到。","love":"感情如龙凤呈祥，和谐美满。","career":"才能得以展现，迎来属于你的高光时刻。","health":"精力如虎，状态极佳，适合开展新计划。"},
]

# 星座元素配对（用于配对占卜）
ELEM_COMPAT = {
    ("火", "火"): (88, "热情碰撞，彼此激励，共同追逐冒险与梦想。两人都充满活力，需注意避免争强好胜。"),
    ("火", "土"): (55, "一个冲动热烈，一个稳重务实，性格互补但节奏差异大，需要用心磨合与包容。"),
    ("火", "风"): (85, "默契天成，思维碰撞产生灿烂火花，相处轻松愉快，充满浪漫与惊喜。"),
    ("火", "水"): (58, "冰火交融，激情与温柔并存；既有强烈吸引，也有不少摩擦，考验双方包容力。"),
    ("土", "土"): (80, "脚踏实地，志同道合，共同构建稳固踏实的生活，是可以相伴一生的伴侣。"),
    ("土", "风"): (50, "一个执着落地，一个飘逸多变，思维方式迥异，需要极大的耐心去理解对方。"),
    ("土", "水"): (88, "土水相生，互相滋养，情感深厚稳定，是最经典的相生组合。"),
    ("风", "风"): (72, "思维活跃，话题永无止境，精神共鸣极强，但较为理性，需培养情感深度。"),
    ("风", "水"): (65, "各有浪漫，但表达方式不同；风象理性，水象感性，需耐心倾听与理解。"),
    ("水", "水"): (83, "情感深邃，心灵相通，共鸣强烈，但容易情绪共振，需要各自保持独立空间。"),
}

# ══════════════════════════════════════════════════════════════════════════════
#  页面配置
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="✦ 神秘占卜馆",
    page_icon="🔮",
    layout="wide",
)

st.markdown("""
<style>
  [data-testid="stAppViewContainer"] { background: #0d0221; }
  [data-testid="stSidebar"] { background: #1a0a2e; }
  [data-testid="stSidebar"] * { color: #e8d5f5 !important; }
  h1, h2, h3 { color: #f1c40f !important; }
  p, li, label { color: #e8d5f5 !important; }
  .stButton > button {
    background: #4a2080; color: #e8d5f5; border: none;
    border-radius: 6px; font-weight: bold;
  }
  .stButton > button:hover { background: #9b59b6; color: #fff; }
  .stTextInput > div > div > input {
    background: #2d1650; color: #e8d5f5; border: 1px solid #9b59b6;
  }
  .card {
    background: #2d1650; border: 1px solid #9b59b6;
    border-radius: 10px; padding: 16px; margin: 8px 0;
  }
  .gold { color: #f1c40f !important; }
  .cyan { color: #00c8c8 !important; }
  .purple { color: #c39bd3 !important; }
  .green { color: #2ecc71 !important; }
  .red { color: #e74c3c !important; }
  .dim { color: #9b7fc0 !important; }
  .stSelectbox > div > div { background: #2d1650; color: #e8d5f5; }
  div[data-testid="stMetricValue"] { color: #f1c40f !important; }
  hr { border-color: #9b59b6; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  侧边栏导航
# ══════════════════════════════════════════════════════════════════════════════
_PAGES = ["🏠 首页", "🃏 塔罗牌占卜", "⭐ 星座今日运势", "☯ 周易占卜", "🔢 数字命理", "🔮 赛博水晶球", "🎋 每日一签"]
if "page_idx" not in st.session_state:
    st.session_state.page_idx = 0

with st.sidebar:
    st.markdown("## 🔮 神秘占卜馆")
    st.markdown(f"<span class='dim'>{date.today().strftime('%Y年%m月%d日')}</span>", unsafe_allow_html=True)
    st.markdown("---")
    page = st.radio(
        "选择占卜方式",
        _PAGES,
        index=st.session_state.page_idx,
        label_visibility="collapsed",
    )
    st.session_state.page_idx = _PAGES.index(page)
    st.markdown("---")
    st.markdown("<span class='dim'>v1.0 · 融合东西方神秘学</span>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  首页
# ══════════════════════════════════════════════════════════════════════════════
if page == "🏠 首页":
    st.markdown("<h1 style='text-align:center'>✦ 神 秘 占 卜 馆 ✦</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;font-style:italic;color:#9b7fc0'>Mystical Divination Chamber</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center;color:#9b7fc0'>今日：{date.today().strftime('%Y年%m月%d日')} · 融合东西方神秘学传统</p>", unsafe_allow_html=True)
    st.markdown("---")

    # 将首页卡片按钮样式化为卡片外观
    st.markdown("""
    <style>
    div[data-testid="column"] .stButton > button {
        background: #2d1650 !important;
        border: 1px solid #9b59b6 !important;
        border-radius: 10px !important;
        padding: 24px 16px !important;
        min-height: 130px !important;
        width: 100% !important;
        white-space: pre-wrap !important;
        text-align: center !important;
        line-height: 1.9 !important;
        font-size: 0.95rem !important;
        color: #e8d5f5 !important;
        transition: border-color 0.2s, background 0.2s !important;
    }
    div[data-testid="column"] .stButton > button:hover {
        background: #3d1a70 !important;
        border-color: #f1c40f !important;
        color: #fff !important;
    }
    </style>
    """, unsafe_allow_html=True)

    cols = st.columns(3)
    modules = [
        ("🃏", "塔罗牌占卜", "三张牌阵 · 过去·现在·未来", "🃏 塔罗牌占卜"),
        ("⭐", "星座今日运势", "十二星座日运 · 综合·爱情·事业·健康", "⭐ 星座今日运势"),
        ("☯", "周易占卜", "铜钱起卦法 · 64卦·爻辞·指引", "☯ 周易占卜"),
        ("🔢", "数字命理", "生命数字解析 · 生命·灵魂·命运", "🔢 数字命理"),
        ("🔮", "赛博水晶球", "神秘指引 · 是非·方向·预言", "🔮 赛博水晶球"),
        ("🎋", "每日一签", "传统签诗 · 今日运势一签知", "🎋 每日一签"),
    ]
    for i, (icon, name, desc, nav_target) in enumerate(modules):
        with cols[i % 3]:
            if st.button(f"{icon}\n{name}\n{desc}", key=f"home_btn_{i}", use_container_width=True):
                st.session_state.page_idx = _PAGES.index(nav_target)
                st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
#  塔罗牌
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🃏 塔罗牌占卜":
    st.markdown("## 🃏 塔罗牌占卜")
    st.markdown("---")

    tarot_mode = st.radio("选择牌阵", ["🌙 每日一卡（快速）", "✦ 三张牌阵（过去·现在·未来）"], horizontal=True)
    name = st.text_input("请在心中默想你的问题，然后输入你的名字：", placeholder="输入名字后点击占卜")

    if tarot_mode == "🌙 每日一卡（快速）":
        if st.button("✦ 抽取今日塔罗 ✦", key="tarot_daily_btn"):
            if not name.strip():
                name = "神秘访客"
            rng = seeded_rng(f"{name}{date.today().isoformat()}daily")
            card = rng.choice(MAJOR_ARCANA)
            rev = rng.choice([True, False])
            rev_text = "🔴 逆位" if rev else "🟢 正位"
            kw_list = card["rev_kw"] if rev else card["up_kw"]
            reading = card["rev"] if rev else card["up"]
            pos_label = "逆位" if rev else "正位"

            col_l, col_c, col_r = st.columns([1, 2, 1])
            with col_c:
                st.markdown(f"""
                <div class='card' style='text-align:center'>
                  <p class='dim' style='margin:0'>今日塔罗 · {date.today().strftime('%Y年%m月%d日')}</p>
                  <div style='font-size:4rem;margin:12px 0'>{card["sym"]}</div>
                  <h2 style='color:#f1c40f !important;margin:4px 0'>{card["zh"]}</h2>
                  <p style='color:#9b7fc0;font-style:italic'>{card["en"]} · {card["roman"]}</p>
                  <p style='color:#9b7fc0;font-size:0.85rem'>🪐 {card["planet"]}　✦ {card["elem"]}象</p>
                  <p style='margin:6px 0'>{rev_text}</p>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("---")
            kw_str = "  ".join(f"`{kw}`" for kw in kw_list)
            st.markdown(f"**关键词：** {kw_str}")
            st.markdown(f"<p style='color:#e8d5f5'>{reading}</p>", unsafe_allow_html=True)
            st.markdown(f"💡 **今日建议：** *{card['adv']}*")
            st.markdown(f"<span class='dim'>今日幸运数字：{card['lucky']}</span>", unsafe_allow_html=True)

    else:
        st.markdown("<span class='dim'>过去 · 现在 · 未来</span>", unsafe_allow_html=True)
    if tarot_mode != "🌙 每日一卡（快速）" and st.button("✦ 开始占卜 ✦", key="tarot_btn"):
        if not name.strip():
            name = "神秘访客"
        rng = seeded_rng(f"{name}{date.today().isoformat()}")
        positions = ["过去（根源）", "现在（核心）", "未来（指引）"]
        pos_colors = ["cyan", "gold", "green"]
        drawn = rng.sample(MAJOR_ARCANA, 3)
        rev_flags = [rng.choice([True, False]) for _ in range(3)]

        # 三张牌横排
        cols = st.columns(3)
        for i, (card, rev) in enumerate(zip(drawn, rev_flags)):
            with cols[i]:
                rev_text = "🔴 逆位" if rev else "🟢 正位"
                st.markdown(f"""
                <div class='card' style='text-align:center'>
                  <p class='{pos_colors[i]}' style='font-weight:bold;margin:0'>{positions[i]}</p>
                  <div style='font-size:2.5rem;margin:8px 0'>{card["sym"]}</div>
                  <p style='color:#e8d5f5;font-weight:bold;font-size:1.1rem;margin:4px 0'>{card["zh"]}</p>
                  <p style='color:#9b7fc0;font-style:italic;font-size:0.85rem;margin:0'>{card["en"]}</p>
                  <p style='color:#9b7fc0;font-size:0.8rem;margin:4px 0'>{card["roman"]} | 🪐{card["planet"]} ✦{card["elem"]}</p>
                  <p style='margin:4px 0'>{rev_text}</p>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("---")

        # 详细解读
        for i, (card, rev) in enumerate(zip(drawn, rev_flags)):
            kw_list = card["rev_kw"] if rev else card["up_kw"]
            reading = card["rev"] if rev else card["up"]
            pos_label = "逆位" if rev else "正位"

            with st.expander(f"{card['sym']} {card['zh']} — {positions[i]} ({pos_label})", expanded=True):
                kw_str = "  ".join(f"`{kw}`" for kw in kw_list)
                st.markdown(f"**关键词：** {kw_str}")
                st.markdown(reading)
                st.markdown(f"💡 **建议：** *{card['adv']}*")

        # 综合
        st.markdown("---")
        st.markdown("### ✨ 综合解读")
        lucky = (drawn[0]["lucky"] + drawn[1]["lucky"] + drawn[2]["lucky"]) % 22
        st.markdown(f"""
        {name}，你今天抽到的是：

        **{drawn[0]["sym"]} {drawn[0]["zh"]}** → **{drawn[1]["sym"]} {drawn[1]["zh"]}** → **{drawn[2]["sym"]} {drawn[2]["zh"]}**

        过去的经历已经塑造了今天的你；当下的状态正是你需要全力应对的核心；
        未来的指引已经浮现，选择权始终在你自己手中。

        <span class='dim'>今日幸运数字：{lucky}</span>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  星座
# ══════════════════════════════════════════════════════════════════════════════
elif page == "⭐ 星座今日运势":
    st.markdown("## ⭐ 十二星座今日运势")
    st.markdown(f"<span class='dim'>日期：{date.today().strftime('%Y年%m月%d日')}</span>", unsafe_allow_html=True)
    st.markdown("---")

    zodiac_names = [f"{z['sym']} {z['name']}" for z in ZODIAC]
    selected = st.selectbox("选择你的星座：", zodiac_names)
    idx = zodiac_names.index(selected)
    z = ZODIAC[idx]

    rng = seeded_rng(f"{z['name']}{date.today().isoformat()}")
    scores = {k: rng.randint(2, 5) for k in ["综合运势", "爱情运势", "事业财运", "健康状态"]}
    gen    = rng.choice(ZODIAC_TEMPLATES["general"])
    love   = rng.choice(ZODIAC_TEMPLATES["love"])
    career = rng.choice(ZODIAC_TEMPLATES["career"])
    health = rng.choice(ZODIAC_TEMPLATES["health"])
    lucky_num = rng.randint(1, 99)
    lucky_colors = ["金色","银色","深红","天蓝","翠绿","紫色","珊瑚橙","玫瑰粉","白色","黑色"]
    l_color = rng.choice(lucky_colors)
    l_hour = rng.choice([f"{rng.randint(8,11)}:00", f"{rng.randint(14,17)}:00", f"{rng.randint(19,22)}:00"])

    # 标题
    st.markdown(f"""
    <div class='card' style='text-align:center'>
      <div style='font-size:3rem'>{z["sym"]}</div>
      <h2 style='color:#f1c40f !important;margin:4px 0'>{z["name"]}  {z["en"]}</h2>
      <p style='color:#9b7fc0'>{z["dates"]} | {z["elem"]}象 | 守护星：{z["ruler"]}</p>
      <p style='color:#9b7fc0;font-style:italic'>{z["trait"]}</p>
    </div>
    """, unsafe_allow_html=True)

    # 评分
    st.markdown("### 今日运势评分")
    cols = st.columns(4)
    for (k, v), col in zip(scores.items(), cols):
        with col:
            st.metric(k, "★" * v + "☆" * (5 - v))

    st.markdown("---")

    # 详情
    for title, text, color in [
        ("✦ 今日综合", gen, "#e8d5f5"),
        ("💕 感情运势", love, "#ff6b9d"),
        ("💼 事业财运", career, "#00c8c8"),
        ("🌿 健康提示", health, "#2ecc71"),
    ]:
        st.markdown(f"#### {title}")
        st.markdown(f"<p style='color:{color}'>{text}</p>", unsafe_allow_html=True)

    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("🔢 幸运数字", str(lucky_num))
    with c2:
        st.metric("🎨 幸运色", l_color)
    with c3:
        st.metric("⏰ 幸运时段", l_hour)

    # ── 星座配对 ──
    st.markdown("---")
    st.markdown("### 💞 星座配对测试")
    zodiac_names2 = [f"{zz['sym']} {zz['name']}" for zz in ZODIAC]
    partner_sel = st.selectbox("选择对方的星座：", zodiac_names2, key="partner_zodiac")
    partner_idx = zodiac_names2.index(partner_sel)
    z2 = ZODIAC[partner_idx]

    e1, e2 = z["elem"], z2["elem"]
    key = (e1, e2) if (e1, e2) in ELEM_COMPAT else (e2, e1)
    score, compat_desc = ELEM_COMPAT.get(key, (70, "两人各有特色，需要用心经营感情。"))

    bar_fill = int(score / 100 * 20)
    bar_str = "█" * bar_fill + "░" * (20 - bar_fill)
    score_color = "#2ecc71" if score >= 80 else "#f1c40f" if score >= 60 else "#e74c3c"

    st.markdown(f"""
    <div class='card'>
      <p style='text-align:center;font-size:1.1rem;color:#e8d5f5;margin:0'>
        {z["sym"]} <b>{z["name"]}</b>（{z["elem"]}象）
        &nbsp;×&nbsp;
        {z2["sym"]} <b>{z2["name"]}</b>（{z2["elem"]}象）
      </p>
      <p style='text-align:center;font-family:monospace;color:{score_color};font-size:1.2rem;margin:8px 0'>{bar_str}</p>
      <p style='text-align:center;font-size:1.8rem;font-weight:bold;color:{score_color};margin:4px 0'>{score}分</p>
      <p style='color:#9b7fc0;text-align:center;margin:4px 0'>{compat_desc}</p>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  周易
# ══════════════════════════════════════════════════════════════════════════════
elif page == "☯ 周易占卜":
    st.markdown("## ☯ 周易占卜 · 铜钱起卦法")
    st.markdown("<span class='dim'>天地之道，唯变是常</span>", unsafe_allow_html=True)
    st.markdown("---")

    question = st.text_input("请在心中默想你的问题：", placeholder="输入你想问的事情")

    if "iching_lines" not in st.session_state:
        st.session_state.iching_lines = []

    # 说明
    st.markdown("""
    <div class='card'>
      <p class='dim' style='margin:0'>
        古法：三枚铜钱连投六次<br>
        正面(字)=阳=3，背面(花)=阴=2<br>
        和=6: 老阴(变爻) &nbsp; 7: 少阳 &nbsp; 8: 少阴 &nbsp; 9: 老阳(变爻)
      </p>
    </div>
    """, unsafe_allow_html=True)

    lines = st.session_state.iching_lines
    n = len(lines)

    # 显示已投结果
    if lines:
        st.markdown("**卦象（从第1爻到第6爻）：**")
        sym_map = {"yang": "━━━━━━━  少阳", "yin": "━━━ ━━━  少阴",
                   "old_yang": "━━━○━━━  老阳(变)", "old_yin": "━━━×━━━  老阴(变)"}
        for i, (ltype, total, coin_str) in enumerate(lines):
            color = "#f1c40f" if "变" in sym_map[ltype] else "#e8d5f5"
            st.markdown(f"<p style='color:{color};font-family:monospace'>第{i+1}爻: {sym_map[ltype]} &nbsp;&nbsp; ({coin_str} 和={total})</p>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        if n < 6:
            if st.button(f"🪙 投出铜钱（第 {n+1} / 6 次）"):
                coins = [random.randint(2, 3) for _ in range(3)]
                total = sum(coins)
                coin_str = " ".join("字" if c == 3 else "花" for c in coins)
                if total == 6:   ltype = "old_yin"
                elif total == 7: ltype = "yang"
                elif total == 8: ltype = "yin"
                else:            ltype = "old_yang"
                st.session_state.iching_lines.append((ltype, total, coin_str))
                st.rerun()
    with col2:
        if st.button("🔄 重新起卦"):
            st.session_state.iching_lines = []
            st.rerun()

    # 显示卦象解读
    if n == 6:
        st.markdown("---")
        lv = [1 if t in (7, 9) else 0 for _, t, _ in lines]
        lo = lv[0] | (lv[1] << 1) | (lv[2] << 2)
        up = lv[3] | (lv[4] << 1) | (lv[5] << 2)

        lo_tri = TRIGRAMS.get(lo, ("未知", "?", "?", "?"))
        up_tri = TRIGRAMS.get(up, ("未知", "?", "?", "?"))
        hex_info = HEXAGRAM_NAMES.get((lo, up))
        if not hex_info:
            rng2 = seeded_rng(f"{lo}{up}")
            hex_info = rng2.choice(list(HEXAGRAM_NAMES.values()))

        hex_name, full_name, core_msg = hex_info
        rng3 = seeded_rng(f"{lo}{up}{date.today().isoformat()}")

        st.markdown(f"""
        <div class='card' style='text-align:center'>
          <h2 class='cyan'>卦象：{full_name}（{lo_tri[1]}{up_tri[1]}）</h2>
          <p class='dim'>上卦：{up_tri[0]}{up_tri[1]}（{up_tri[2]}） | 下卦：{lo_tri[0]}{lo_tri[1]}（{lo_tri[2]}）</p>
        </div>
        """, unsafe_allow_html=True)

        # 卦形（从上到下显示第6爻到第1爻）
        sym_map2 = {"yang": "━━━━━━━━━  (阳爻)", "yin": "━━━   ━━━  (阴爻)",
                    "old_yang": "━━━ ○ ━━━  (老阳·变)", "old_yin": "━━━ × ━━━  (老阴·变)"}
        st.markdown("**卦形：**")
        for i in range(5, -1, -1):
            ltype, _, _ = lines[i]
            color = "#f1c40f" if "变" in sym_map2[ltype] else "#e8d5f5"
            st.markdown(f"<p style='color:{color};font-family:monospace;margin:2px 0'>第{i+1}爻  {sym_map2[ltype]}</p>", unsafe_allow_html=True)

        st.markdown("---")

        q = question.strip() or "所问之事"
        readings = [
            f"此卦上卦为{up_tri[0]}（{up_tri[1]}），象征{up_tri[2]}，代表{up_tri[3]}；下卦为{lo_tri[0]}（{lo_tri[1]}），象征{lo_tri[2]}，代表{lo_tri[3]}。两者相合，卦名「{hex_name}」，{core_msg}。",
            f"卦象显示，当前局势正处于一个{'转折' if rng3.random()>0.5 else '积累'}的关键节点。{'宜主动出击，把握时机；' if rng3.random()>0.5 else '宜沉静待机，蓄势待发；'}{'切忌急功近利，欲速则不达。' if rng3.random()>0.5 else '切忌犹豫不决，坐失良机。'}",
            f"就{q}而言，天时{'在你这边' if rng3.random()>0.5 else '尚未成熟'}，地利{'已经具备' if rng3.random()>0.5 else '需要进一步创造'}，人和{'是当前最需关注的关键因素。' if rng3.random()>0.5 else '是你最大的优势所在。'}",
        ]
        for r in readings:
            st.markdown(f"<div class='card'><p style='color:#e8d5f5;margin:0'>{r}</p></div>", unsafe_allow_html=True)

        advices = [
            "守正待时，不失其正；机来则动，动必有成。",
            "顺天应人，刚柔相济；内省自修，方可外显。",
            "道法自然，无为而无不为；知止而后有定。",
            "厚德载物，自强不息；知常容，容乃公。",
        ]
        st.markdown(f"""
        <div class='card'>
          <p class='gold' style='font-weight:bold'>爻辞建议</p>
          <p style='color:#e8d5f5;font-style:italic'>{rng3.choice(advices)}</p>
          <p class='dim'>卦名「{hex_name}」的核心智慧：{core_msg}</p>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  数字命理
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🔢 数字命理":
    st.markdown("## 🔢 数字命理 · 生命数字解析")
    st.markdown("<span class='dim'>毕达哥拉斯数字神秘学</span>", unsafe_allow_html=True)
    st.markdown("---")

    birth = st.text_input("出生日期 (YYYYMMDD)：", value="19950315", max_chars=8)

    if st.button("✦ 开始解析 ✦", key="num_btn"):
        try:
            dt = datetime.strptime(birth.strip(), "%Y%m%d")
        except ValueError:
            st.error("请输入正确日期格式，例如：19950315")
            st.stop()

        def reduce(n):
            if n in (11, 22, 33): return n
            while n > 9:
                n = sum(int(d) for d in str(n))
                if n in (11, 22, 33): return n
            return n

        digits    = [int(c) for c in birth if c.isdigit()]
        life_path = reduce(sum(digits))
        soul      = reduce(sum(int(c) for c in str(dt.day) + str(dt.month)))
        destiny   = reduce(sum(int(c) for c in str(dt.year) + str(dt.month) + str(dt.day)))
        data      = NUMEROLOGY.get(life_path, NUMEROLOGY[1])
        soul_data = NUMEROLOGY.get(soul, NUMEROLOGY[1])

        st.markdown(f"""
        <div class='card' style='text-align:center'>
          <h2 class='green'>{data["symbol"]}  {data["title"]}  {data["symbol"]}</h2>
          <p class='dim'>出生：{dt.strftime("%Y年%m月%d日")}</p>
        </div>
        """, unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        with c1: st.metric("生命数字", str(life_path))
        with c2: st.metric("灵魂数字", str(soul))
        with c3: st.metric("命运数字", str(destiny))

        st.markdown("---")
        st.markdown(f"### 生命数字 {life_path} 完整解析")
        st.markdown(f"**✦ 核心特质**\n\n{data['trait']}")
        st.markdown(f"**🎯 人生使命**\n\n{data['mission']}")
        st.markdown(f"**⚔ 主要挑战**\n\n{data['challenge']}")
        st.markdown(f"**💎 幸运加持**\n\n幸运颜色：{data['lucky_color']}　　守护宝石：{data['lucky_stone']}")

        if soul != life_path:
            st.markdown("---")
            st.markdown(f"### {soul_data['symbol']} 灵魂数字 {soul}")
            st.markdown(f"<span class='dim'>{soul_data['trait'][:100]}…</span>", unsafe_allow_html=True)

        # 个人年
        this_year = date.today().year
        py = reduce(sum(int(c) for c in str(dt.month) + str(dt.day) + str(this_year)))
        py_meanings = {
            1:"新周期的开始，播种新想法与计划的一年。",
            2:"关系与合作的一年，耐心等待，细心经营。",
            3:"创造力爆发的一年，表达自我，扩展社交圈。",
            4:"建造与稳固的一年，脚踏实地，打好基础。",
            5:"自由与变化的一年，冒险探索，突破舒适区。",
            6:"责任与家庭的一年，服务他人，收获感恩。",
            7:"内省与灵性成长的一年，深化智慧，寻找真相。",
            8:"丰收与成就的一年，努力付出换来实质回报。",
            9:"完成与释放的一年，放下旧的，为新周期清空。",
            11:"灵感迸发的一年，直觉力极强，灵性突破时机。",
            22:"宏大建造的一年，将梦想系统性地落实为现实。",
            33:"大爱与教导的一年，用慈悲影响周围的一切。",
        }
        st.markdown("---")
        st.markdown(f"### {this_year}年 个人年数字：{py}")
        st.markdown(py_meanings.get(py, "一个充满潜力的年份。"))


# ══════════════════════════════════════════════════════════════════════════════
#  赛博水晶球
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🔮 赛博水晶球":
    st.markdown("## 🔮 赛博水晶球 · 神秘指引")
    st.markdown("<span class='dim'>宇宙的智慧，通过量子随机性传达</span>", unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("""
    <div style='text-align:center;font-size:5rem;margin:8px 0'>🔮</div>
    <p style='text-align:center;color:#9b7fc0'>向水晶球提问，获得宇宙的指引</p>
    """, unsafe_allow_html=True)

    question = st.text_input("向水晶球提问（是/否类问题）：", placeholder="例如：我现在的决定是正确的吗？")

    answers_yes = [
        "✨ 宇宙的能量明确指向：是的。",
        "🌟 星辰排列支持这个方向，继续前进。",
        "☀ 水晶球闪耀着金色光芒：时机已到。",
        "🎯 命运之线正在向这个结果汇聚。",
        "💫 一切迹象都在说：是的，相信自己。",
        "🌸 宇宙在微笑着点头。",
        "⭐ 这个选择与你的最高利益对齐。",
    ]
    answers_maybe = [
        "🌫 水晶球中迷雾弥漫，结果尚未确定。",
        "⚖ 能量正在校准中，稍后再问会更清晰。",
        "🌙 月相不够明朗，再思考一下。",
        "🔄 宇宙说：这取决于你接下来的行动。",
        "🌊 如海浪般起伏，无法确定，但充满可能。",
        "🎭 答案在你内心深处，向内寻找。",
    ]
    answers_no = [
        "🌑 水晶球笼罩在阴影中：此路不通。",
        "⛈ 能量在这个方向受阻，重新考虑吧。",
        "🌀 宇宙建议：不是现在，也许将来。",
        "🚫 深红色的光芒提示：谨慎行事。",
        "💨 像风一样飘散——这个选择不够稳固。",
    ]
    answers_all = answers_yes * 4 + answers_maybe * 2 + answers_no * 2

    if "crystal_history" not in st.session_state:
        st.session_state.crystal_history = []

    if st.button("🔮 感应宇宙", key="crystal_btn"):
        if question.strip():
            rng = seeded_rng(f"{question}{datetime.now().strftime('%Y%m%d%H')}")
            answer = rng.choice(answers_all)
            st.session_state.crystal_history.append((question.strip(), answer))
        else:
            st.warning("请先输入问题")

    if st.session_state.crystal_history:
        last_q, last_a = st.session_state.crystal_history[-1]
        st.markdown(f"""
        <div class='card' style='text-align:center'>
          <p class='dim'>问：{last_q}</p>
          <h3 style='color:#e8d5f5'>{last_a}</h3>
        </div>
        """, unsafe_allow_html=True)

        if len(st.session_state.crystal_history) > 1:
            st.markdown("---")
            st.markdown("**占问记录**")
            for q, a in reversed(st.session_state.crystal_history[:-1]):
                st.markdown(f"<p class='dim'>问：{q}<br>答：{a}</p>", unsafe_allow_html=True)

    if st.button("清空记录"):
        st.session_state.crystal_history = []
        st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
#  每日一签
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🎋 每日一签":
    st.markdown("## 🎋 每日一签")
    st.markdown("<span class='dim'>传统签诗 · 每日一签，问问今天的运势</span>", unsafe_allow_html=True)
    st.markdown("---")

    name_qian = st.text_input("请输入你的名字（影响今日签文）：", placeholder="输入名字，每天一签")

    if st.button("🎋 摇签求签", key="fortune_btn"):
        if not name_qian.strip():
            name_qian = "神秘访客"
        rng = seeded_rng(f"{name_qian}{date.today().isoformat()}")
        slip = rng.choice(FORTUNE_SLIPS)

        grade_color = {
            "上上签": "#f1c40f",
            "上签": "#2ecc71",
            "中上签": "#00c8c8",
            "中签": "#e8d5f5",
            "中下签": "#e67e22",
            "下签": "#e74c3c",
        }.get(slip["grade"], "#e8d5f5")

        st.markdown(f"""
        <div class='card' style='text-align:center'>
          <p class='dim' style='margin:0'>{date.today().strftime('%Y年%m月%d日')} · {name_qian}的今日签</p>
          <div style='font-size:3rem;margin:8px 0'>🎋</div>
          <p style='color:{grade_color};font-size:1.5rem;font-weight:bold;margin:4px 0'>{slip["grade"]}</p>
          <h2 style='color:#f1c40f !important;margin:4px 0'>第{slip["num"]}签 · {slip["title"]}</h2>
          <div style='border-top:1px solid #9b59b6;margin:12px 40px;padding-top:12px'>
            <p style='color:#c39bd3;font-style:italic;font-size:1.05rem;margin:0'>{slip["poem"]}</p>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        cols_q = st.columns(2)
        items = [
            ("✦ 总体运势", slip["general"], "#e8d5f5"),
            ("💕 感情姻缘", slip["love"], "#ff6b9d"),
            ("💼 事业财运", slip["career"], "#00c8c8"),
            ("🌿 健康提示", slip["health"], "#2ecc71"),
        ]
        for i, (title, text, color) in enumerate(items):
            with cols_q[i % 2]:
                st.markdown(f"""
                <div class='card'>
                  <p class='gold' style='font-weight:bold;margin:0 0 6px 0'>{title}</p>
                  <p style='color:{color};margin:0'>{text}</p>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown(f"<p class='dim' style='text-align:center'>签文每日根据姓名与日期生成，明日再来可抽取新签。</p>", unsafe_allow_html=True)
