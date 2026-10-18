function openCardPage(imageUrl) {
    window.location.href = `Newyearcard.html?background=${encodeURIComponent(imageUrl)}`;
  }
  
//------------------------------------------------------------------------------------------------------------------------------------------------------------
// 生成烟花的粒子效果
function createFirework() {
    const numberOfParticles = 60; // 每个烟花的粒子数量
    const colors = ['#FF5733', '#FFC300', '#DAF7A6', '#FF33FF', '#33FFFC', '#FF5733'];
    const fireworkContainer = document.createElement('div');
    
    fireworkContainer.style.position = 'absolute';
    fireworkContainer.style.left = `${Math.random() * window.innerWidth}px`;
    fireworkContainer.style.top = `${Math.random() * window.innerHeight}px`;
    document.getElementById('background-effect').appendChild(fireworkContainer);
  
    for (let i = 0; i < numberOfParticles; i++) {
      const particle = document.createElement('div');
      particle.classList.add('firework-particle');
  
      // 随机分配颜色
      particle.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
  
      // 随机角度和距离
      const angle = Math.random() * 2 * Math.PI;
      const distance = Math.random() * 80 + 20; // 粒子扩散的范围
  
      // 设置自定义属性，用于CSS动画
      particle.style.setProperty('--x', `${Math.cos(angle) * distance}px`);
      particle.style.setProperty('--y', `${Math.sin(angle) * distance}px`);
  
      fireworkContainer.appendChild(particle);
    }
  
    // 移除烟花效果
    setTimeout(() => {
      fireworkContainer.remove();
    }, 1500);
  }
  
  // 每隔一定时间生成一个烟花
  setInterval(createFirework, 500);
  
  