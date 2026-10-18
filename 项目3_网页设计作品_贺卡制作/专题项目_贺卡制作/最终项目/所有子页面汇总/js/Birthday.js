function openCardPage(imageUrl) {
  window.location.href = `Birthdaycard.html?background=${encodeURIComponent(imageUrl)}`;
}

//------------------------------------------------------------------------------------------------------------------------------------------------------------

const giftContainer = document.getElementById('gift-container');  
for (let i = 0; i < 15; i++) {  
  const gift = document.createElement('div');  
  gift.className = 'gift';  
  // 随机设置gift元素的初始位置  
  gift.style.top = `${Math.random() * 100}%`;  
  gift.style.left = `${Math.random() * 100}%`;  
  // 为每个gift元素设置不同的动画延迟，使飘动效果更加自然  
  gift.style.animationDelay = `${Math.random() * 8}s`;  
  // 可以选择性地为gift添加不同的颜色或大小  
    
  gift.style.width = `${Math.random() * 150 + 50}px`;  
  gift.style.height = `${Math.random() * 140 + 70}px`;  
  giftContainer.appendChild(gift);  
}  



