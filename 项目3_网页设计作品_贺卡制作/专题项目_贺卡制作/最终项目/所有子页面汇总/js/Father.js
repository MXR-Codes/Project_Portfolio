function openCardPage(imageUrl) {
    window.location.href = `Fathercard.html?background=${encodeURIComponent(imageUrl)}`;
  }
  
//------------------------------------------------------------------------------------------------------------------------------------------------------------
// 生成烟花的粒子效果
const balloonContainer = document.getElementById('balloon-container');  
  for (let i = 0; i < 15; i++) {  
    const balloon = document.createElement('div');  
    balloon.className = 'balloon';  
    // 随机设置气球元素的初始位置  
    balloon.style.top = `${Math.random() * 100}%`;  
    balloon.style.left = `${Math.random() * 100}%`;  
    // 为每个气球元素设置不同的动画延迟，使飘动效果更加自然  
    balloon.style.animationDelay = `${Math.random() * 8}s`;  
    // 可以选择性地为气球添加不同的颜色或大小  
      
    balloon.style.width = `${Math.random() * 150 + 50}px`;  
    balloon.style.height = `${Math.random() * 140 + 70}px`;  
    balloonContainer.appendChild(balloon);  
  }  
  

  
  