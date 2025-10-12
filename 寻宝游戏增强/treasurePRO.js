class GameState {
    constructor() {
        // 游戏状态变量
        this.visitedLocations = [];
        this.currentScene = null; // e.g. 'library'
        this.hasAncientMap = false;
        this.hasDirection = false;
        this.hasCrossedDesert = false;
        this.hasFoundTreasure = false;

        // 背景音乐映射
        this.musicFiles = {
            'library': './audio/library.mp3',
            'signpost': './audio/signpost.mp3',
            'desert-road': './audio/desert.mp3',
            'temple': './audio/temple.mp3',
            'index': './audio/background.mp3'
        };
        this.backgroundMusic = null;
        this.volume = 0.5;
    }

    // 向后兼容的方法名（保持API一致）
    loadState() { return this.load(); }
    saveState() { return this.save(); }
    resetState() { return this.reset(); }

    // 加载游戏状态
    load() {
        try {
            const raw = localStorage.getItem('treasureGameState');
            if (!raw) return this;
            const s = JSON.parse(raw);
            this.visitedLocations = s.visitedLocations || [];
            this.currentScene = s.currentScene || null;
            this.hasAncientMap = !!s.hasAncientMap;
            this.hasDirection = !!s.hasDirection;
            this.hasCrossedDesert = !!s.hasCrossedDesert;
            this.hasFoundTreasure = !!s.hasFoundTreasure;
        } catch (e) {
            console.warn('loadState failed, using defaults', e);
        }
        return this;
    }

    // 保存游戏状态
    save() {
        try {
            localStorage.setItem('treasureGameState', JSON.stringify({
                visitedLocations: this.visitedLocations,
                currentScene: this.currentScene,
                hasAncientMap: this.hasAncientMap,
                hasDirection: this.hasDirection,
                hasCrossedDesert: this.hasCrossedDesert,
                hasFoundTreasure: this.hasFoundTreasure
            }));
        } catch (e) {
            console.warn('saveState failed', e);
        }
    }

    // 重置游戏状态
    reset() {
        localStorage.removeItem('treasureGameState');
        this.visitedLocations = [];
        this.currentScene = null;
        this.hasAncientMap = false;
        this.hasDirection = false;
        this.hasCrossedDesert = false;
        this.hasFoundTreasure = false;
        if (this.backgroundMusic) {
            try { this.backgroundMusic.pause(); } catch (e) {}
            this.backgroundMusic = null;
        }
    }

    // 标记位置已访问
    markVisited(key) {
        if (!this.visitedLocations.includes(key)) {
            this.visitedLocations.push(key);
            this.save();
        }
    }

    // 播放背景音乐
    playBackgroundMusic(key) {
        try {
            const src = this.musicFiles[key];
            if (!src) return;
            
            // 停止当前音乐
            if (this.backgroundMusic) {
                this.backgroundMusic.pause();
                this.backgroundMusic = null;
            }
            
            // 创建并播放新音乐
            const a = new Audio(src);
            a.loop = true;
            a.volume = this.volume;
            a.play().catch(() => { /* autoplay restrictions: 忽略 */ });
            this.backgroundMusic = a;
            
            // 更新音乐按钮状态
            this.updateMusicButton();
        } catch (e) {
            console.warn('playBackgroundMusic failed', e);
        }
    }

    // 更新音乐按钮状态
    updateMusicButton() {
        const musicButton = document.querySelector('.music-button');
        if (musicButton) {
            musicButton.textContent = this.backgroundMusic && !this.backgroundMusic.paused ? '🔊' : '🔇';
        }
    }

    // 页面导航和音乐控制功能
    setupNavigation() {
        // 绑定位置按钮事件
        document.querySelectorAll('.location-button').forEach(btn => {
            btn.addEventListener('click', () => {
                const loc = btn.getAttribute('data-location') || btn.textContent.trim();
                const sceneFile = `${loc}.html`;
                navigateToScene(sceneFile);
            });
        });

        // 绑定返回按钮事件
        document.querySelectorAll('.return-button').forEach(b => {
            b.addEventListener('click', () => {
                // 添加渐隐过渡
                document.body.style.transition = 'opacity 0.4s';
                document.body.style.opacity = '0';
                setTimeout(() => { 
                    window.location.href = 'index.html'; 
                }, 420);
            });
        });
        
        // 创建音乐控制按钮
        const musicButton = document.createElement('button');
        musicButton.className = 'music-button';
        musicButton.textContent = this.backgroundMusic ? '🔊' : '🔇';
        
        // 设置按钮样式
        Object.assign(musicButton.style, {
            position: 'fixed',
            top: '20px',
            right: '20px',
            zIndex: '1000',
            padding: '10px',
            borderRadius: '50%',
            border: 'none',
            cursor: 'pointer',
            background: 'rgba(107, 76, 47, 0.8)',
            fontSize: '20px',
            boxShadow: '0 2px 8px rgba(0, 0, 0, 0.3)',
            transition: 'all 0.3s ease',
            minWidth: '44px',
            height: '44px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
        });
        
        // 添加到页面
        document.body.appendChild(musicButton);
        
        // 添加音乐控制事件
        musicButton.addEventListener('click', () => {
            if (this.backgroundMusic) {
                if (this.backgroundMusic.paused) {
                    this.backgroundMusic.play().catch(e => console.log('无法播放音乐:', e));
                    musicButton.textContent = '🔊';
                } else {
                    this.backgroundMusic.pause();
                    musicButton.textContent = '🔇';
                }
            }
        });
        
        // 添加音量控制功能
        let volumeControlVisible = false;
        const volumeSlider = document.createElement('input');
        volumeSlider.type = 'range';
        volumeSlider.min = '0';
        volumeSlider.max = '1';
        volumeSlider.step = '0.1';
        volumeSlider.value = this.volume;
        
        Object.assign(volumeSlider.style, {
            position: 'fixed',
            top: '70px',
            right: '20px',
            zIndex: '1001',
            width: '100px',
            display: 'none',
            transform: 'rotate(-90deg) translate(20px, 0)',
            transformOrigin: 'right bottom'
        });
        
        document.body.appendChild(volumeSlider);
        
        volumeSlider.addEventListener('input', () => {
            this.volume = parseFloat(volumeSlider.value);
            if (this.backgroundMusic) {
                this.backgroundMusic.volume = this.volume;
            }
        });
        
        // 显示/隐藏音量控制
        musicButton.addEventListener('contextmenu', (e) => {
            e.preventDefault();
            volumeControlVisible = !volumeControlVisible;
            volumeSlider.style.display = volumeControlVisible ? 'block' : 'none';
        });
        
        // 点击其他地方关闭音量控制
        document.addEventListener('click', (e) => {
            if (!musicButton.contains(e.target) && !volumeSlider.contains(e.target)) {
                volumeControlVisible = false;
                volumeSlider.style.display = 'none';
            }
        });
        
        // 悬停效果
        musicButton.addEventListener('mouseover', () => {
            musicButton.style.transform = 'scale(1.1)';
            musicButton.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.4)';
        });
        
        musicButton.addEventListener('mouseout', () => {
            musicButton.style.transform = 'scale(1)';
            musicButton.style.boxShadow = '0 2px 8px rgba(0, 0, 0, 0.3)';
        });
    }
}

// 寻宝过程API类，管理所有异步寻宝事件
class TreasureMap {
    // 获取初始线索
    static getInitialClue() {
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve('你在铜封古籍中找到一张残缺的古地图的碎片。');
            }, 1000);
        });
    }

    // 解码古代文字
    static decodeAncientScript(clue) {
        return new Promise((resolve, reject) => {
            setTimeout(() => {
                if (!clue) { 
                    reject('没有线索可以解码'); 
                    return; 
                }
                resolve('解码完成：地图提示先去路标确认方向，再沿古道前往神庙。');
            }, 1200);
        });
    }

    // 获取下一步方向
    static nextStep() {
        return new Promise((resolve) => {
            setTimeout(() => {
                const random = Math.random();
                if (random < 0.2) {
                    resolve({ 
                        direction: null, 
                        message: '路标上的符号模糊不清，暂时无法确定方向。' 
                    });
                } else {
                    resolve({ 
                        direction: '向东南方', 
                        message: '路标与古地图对应，指向东南方古道。' 
                    });
                }
            }, 800);
        });
    }

    // 穿越沙漠
    static traverseDesert(direction) {
        return new Promise((resolve, reject) => {
            setTimeout(() => {
                if (!direction) { 
                    reject('没有方向，迷失在古道'); 
                    return; 
                }
                resolve('你成功穿越风沙古道，看到了神庙轮廓');
            }, 1200);
        });
    }

    // 在神庙中搜索宝藏（可能遇到守卫）
    static searchTemple(location) {
        return new Promise((resolve, reject) => {
            setTimeout(() => {
                const r = Math.random();
                if (r < 0.5) { 
                    reject('遭遇守卫'); 
                } else { 
                    resolve('发现了宝箱'); 
                }
            }, 1000);
        });
    }

    // 打开宝箱
    static openTreasureBox() {
        return new Promise((resolve) => {
            setTimeout(() => resolve('你打开了宝箱：获得秘宝'), 700);
        });
    }
}

// 增强的UI辅助函数：toast与modal
function showToast(text, duration = 2000, type = 'info') {
    // 移除任何现有toast
    const existingToast = document.querySelector('.toast-notification');
    if (existingToast) existingToast.remove();
    
    const t = document.createElement('div');
    t.className = 'toast-notification';
    t.textContent = text;
    
    // 根据类型设置不同背景色
    const bgColors = {
        info: 'rgba(0,0,0,0.7)',
        success: 'rgba(34,139,34,0.8)',
        error: 'rgba(139,0,0,0.8)',
        warning: 'rgba(255,140,0,0.8)'
    };
    
    Object.assign(t.style, {
        position: 'fixed', 
        left: '50%', 
        top: '20%', 
        transform: 'translateX(-50%)',
        background: bgColors[type] || bgColors.info,
        color: '#fff', 
        padding: '12px 20px', 
        borderRadius: '8px', 
        zIndex: 9999,
        boxShadow: '0 4px 12px rgba(0,0,0,0.3)',
        fontFamily: 'Arial, sans-serif',
        fontSize: '16px',
        transition: 'opacity 0.3s, transform 0.3s',
        transform: 'translateX(-50%) translateY(0)',
        animation: 'slideDown 0.3s ease-out'
    });
    
    // 添加动画样式
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideDown {
            from { transform: translateX(-50%) translateY(-20px); opacity: 0; }
            to { transform: translateX(-50%) translateY(0); opacity: 1; }
        }
    `;
    document.head.appendChild(style);
    
    document.body.appendChild(t);
    
    // 定时移除
    setTimeout(() => {
        t.style.transition = 'opacity 0.3s, transform 0.3s';
        t.style.opacity = '0';
        t.style.transform = 'translateX(-50%) translateY(-20px)';
        setTimeout(() => {
            t.remove();
            style.remove();
        }, 300);
    }, duration);
}

function showModal(message, buttonText = '确认', onConfirm, cancelButtonText = null, onCancel = null) {
    // 创建模态框元素
    const overlay = document.createElement('div');
    const box = document.createElement('div');
    const p = document.createElement('p');
    const btn = document.createElement('button');
    
    // 设置样式
    Object.assign(overlay.style, {
        position: 'fixed', 
        left: 0, 
        top: 0, 
        right: 0, 
        bottom: 0, 
        background: 'rgba(0,0,0,0.6)', 
        display: 'flex', 
        alignItems: 'center', 
        justifyContent: 'center', 
        zIndex: 10000,
        animation: 'fadeIn 0.3s ease-out'
    });
    
    Object.assign(box.style, {
        width: '90%',
        maxWidth: '400px',
        padding: '24px', 
        background: '#F9F5F0', 
        color: '#6B4C2F', 
        border: '3px solid #C8A56B', 
        borderRadius: '12px', 
        textAlign: 'center',
        boxShadow: '0 10px 30px rgba(0,0,0,0.4)',
        animation: 'scaleIn 0.3s ease-out'
    });
    
    Object.assign(p.style, {
        marginBottom: '20px',
        lineHeight: '1.6',
        fontSize: '16px'
    });
    
    Object.assign(btn.style, {
        background: '#6B4C2F', 
        color: '#F9F5F0', 
        border: 'none', 
        padding: '10px 20px', 
        borderRadius: '6px', 
        cursor: 'pointer',
        fontSize: '16px',
        fontWeight: 'bold',
        transition: 'all 0.2s ease',
        margin: '0 5px'
    });
    
    // 添加动画样式
    const style = document.createElement('style');
    style.textContent = `
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        @keyframes scaleIn {
            from { transform: scale(0.9); opacity: 0; }
            to { transform: scale(1); opacity: 1; }
        }
    `;
    document.head.appendChild(style);
    
    // 设置内容
    p.textContent = message;
    btn.textContent = buttonText;
    
    // 创建按钮容器
    const buttonContainer = document.createElement('div');
    buttonContainer.style.display = 'flex';
    buttonContainer.style.justifyContent = 'center';
    buttonContainer.style.gap = '10px';
    
    // 添加确认按钮
    buttonContainer.appendChild(btn);
    
    // 添加取消按钮（如果提供）
    if (cancelButtonText) {
        const cancelBtn = document.createElement('button');
        Object.assign(cancelBtn.style, {
            background: '#C8A56B', 
            color: '#F9F5F0', 
            border: 'none', 
            padding: '10px 20px', 
            borderRadius: '6px', 
            cursor: 'pointer',
            fontSize: '16px',
            fontWeight: 'bold',
            transition: 'all 0.2s ease',
            margin: '0 5px'
        });
        cancelBtn.textContent = cancelButtonText;
        buttonContainer.appendChild(cancelBtn);
        
        cancelBtn.addEventListener('click', () => {
            document.body.removeChild(overlay);
            style.remove();
            if (typeof onCancel === 'function') onCancel();
        });
    }
    
    // 组装并添加到页面
    box.appendChild(p);
    box.appendChild(buttonContainer);
    overlay.appendChild(box);
    document.body.appendChild(overlay);
    
    // 确认按钮事件
    btn.addEventListener('click', () => {
        document.body.removeChild(overlay);
        style.remove();
        if (typeof onConfirm === 'function') onConfirm();
    });
    
    // 按钮悬停效果
    btn.addEventListener('mouseover', () => {
        btn.style.transform = 'translateY(-2px)';
        btn.style.boxShadow = '0 4px 10px rgba(0,0,0,0.2)';
    });
    
    btn.addEventListener('mouseout', () => {
        btn.style.transform = 'translateY(0)';
        btn.style.boxShadow = 'none';
    });
}

// 辅助函数：获取元素
function getElement(id) {
    const element = document.getElementById(id);
    if (!element) {
        console.warn(`Element with id '${id}' not found`);
    }
    return element;
}

// 场景切换，确保按游戏流程进行
function navigateToScene(sceneFile) {
    const state = new GameState().load();
    
    // 场景访问条件映射
    const accessConditions = {
        'signpost.html': () => state.hasAncientMap,
        'desert-road.html': () => state.hasDirection,
        'temple.html': () => state.hasCrossedDesert
    };
    
    // 检查访问条件
    const conditionChecker = accessConditions[sceneFile];
    if (conditionChecker && !conditionChecker()) {
        showModal(
            '当前缺少必要条件，建议按顺序进行：图书馆 → 沙漠路标 → 风沙古道 → 神庙正门。返回地图选择下一步。', 
            '返回地图', 
            () => { window.location.href = 'index.html'; },
            '取消',
            null
        );
        return false;
    }
    
    // 记录当前场景
    const sceneKey = sceneFile.replace('.html', '');
    state.currentScene = sceneKey;
    state.markVisited(sceneKey);
    
    // 添加过渡效果
    document.body.style.transition = 'opacity 0.5s ease';
    document.body.style.opacity = '0';
    
    // 延迟跳转，等待过渡效果完成
    setTimeout(() => {
        window.location.href = sceneFile;
    }, 500);
    
    return true;
}

// 导出到全局，供页面脚本调用
window.GameState = GameState;
window.TreasureMap = TreasureMap;
window.navigateToScene = navigateToScene;
window.showToast = showToast;
window.showModal = showModal;
window.getElement = getElement;

// 添加静态方法load到GameState类，与index.html中的调用保持一致
GameState.load = function() {
    const gameState = new GameState();
    return gameState.loadState();
};

// 添加辅助类：游戏动画管理
class AnimationManager {
    static fadeIn(element, duration = 500) {
        element.style.opacity = '0';
        element.style.transition = `opacity ${duration}ms ease`;
        element.style.display = 'block';
        
        // 触发重排
        void element.offsetWidth;
        
        element.style.opacity = '1';
        
        return new Promise(resolve => {
            setTimeout(resolve, duration);
        });
    }
    
    static fadeOut(element, duration = 500) {
        element.style.transition = `opacity ${duration}ms ease`;
        element.style.opacity = '0';
        
        return new Promise(resolve => {
            setTimeout(() => {
                element.style.display = 'none';
                resolve();
            }, duration);
        });
    }
    
    static pulse(element, duration = 2000, iterations = Infinity) {
        element.style.animation = `pulse ${duration}ms ease-in-out ${iterations}`;
        
        // 添加动画样式如果不存在
        if (!document.querySelector('#pulseAnimation')) {
            const style = document.createElement('style');
            style.id = 'pulseAnimation';
            style.textContent = `
                @keyframes pulse {
                    0%, 100% { transform: scale(1); }
                    50% { transform: scale(1.05); }
                }
            `;
            document.head.appendChild(style);
        }
    }
    
    static stopAnimation(element) {
        element.style.animation = 'none';
    }
};

// 导出动画管理器
window.AnimationManager = AnimationManager;