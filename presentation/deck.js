/* 簡報引擎：←/→ 換頁、F 全螢幕、M 目錄、點「試題」顯示答案 */
(function(){
  var stage=document.getElementById('stage');
  var slides=[].slice.call(document.querySelectorAll('.slide'));
  var bar=document.getElementById('progress');
  var cur=0;

  function fit(){
    var s=Math.min(window.innerWidth/1280,window.innerHeight/720);
    stage.style.transform='scale('+s+')';
  }
  function show(i,push){
    i=Math.max(0,Math.min(slides.length-1,i));
    slides[cur].classList.remove('active');
    cur=i; slides[cur].classList.add('active');
    var bd=slides[cur].querySelector('.bd'); if(bd) bd.scrollTop=0;
    bar.style.width=((cur+1)/slides.length*100)+'%';
    var pg=slides[cur].querySelector('.pg'); if(pg) pg.textContent=(cur+1)+' / '+slides.length;
    updateMore();
    if(push!==false){ try{history.replaceState(null,'','#'+(cur+1));}catch(e){} }
  }
  function updateMore(){
    var s=slides[cur], bd=s.querySelector('.bd');
    if(bd && bd.scrollHeight-bd.clientHeight>8 && bd.scrollTop+bd.clientHeight<bd.scrollHeight-8) s.classList.add('more');
    else s.classList.remove('more');
  }
  slides.forEach(function(s){
    var bd=s.querySelector('.bd'); if(!bd||bd.classList.contains('noscroll'))return;
    var h=document.createElement('div'); h.className='morehint'; h.textContent='↓ 往下捲動（滾輪或 ↓ 鍵）'; s.appendChild(h);
    bd.addEventListener('scroll',updateMore);
  });
  function scrollBd(dy){var bd=slides[cur].querySelector('.bd'); if(bd) bd.scrollBy({top:dy,behavior:'smooth'});}
  function next(){
    // 先逐一展開「試題」答案，再換頁
    var q=slides[cur].querySelector('.quiz-item:not(.open)');
    if(q && slides[cur].classList.contains('quiz-slide')){q.classList.add('open');return;}
    show(cur+1);
  }
  function prev(){show(cur-1);}

  document.addEventListener('keydown',function(e){
    var k=e.key;
    if(k==='ArrowRight'||k==='PageDown'||k===' '||k==='Enter'){e.preventDefault();next();}
    else if(k==='ArrowLeft'||k==='PageUp'||k==='Backspace'){e.preventDefault();prev();}
    else if(k==='ArrowDown'){e.preventDefault();scrollBd(320);}
    else if(k==='ArrowUp'){e.preventDefault();scrollBd(-320);}
    else if(k==='Home')show(0);
    else if(k==='End')show(slides.length-1);
    else if(k==='f'||k==='F'){ if(document.fullscreenElement)document.exitFullscreen(); else document.documentElement.requestFullscreen&&document.documentElement.requestFullscreen(); }
    else if(k==='m'||k==='M'||k==='Escape'){toggleMenu();}
  });
  // 點試題顯示/隱藏答案
  document.addEventListener('click',function(e){
    var q=e.target.closest&&e.target.closest('.quiz-item'); if(q){q.classList.toggle('open');}
  });
  // 觸控滑動
  var sx=null;
  document.addEventListener('touchstart',function(e){sx=e.touches[0].clientX;},{passive:true});
  document.addEventListener('touchend',function(e){
    if(sx===null)return; var dx=e.changedTouches[0].clientX-sx; sx=null;
    if(Math.abs(dx)>60){dx<0?next():prev();}
  });
  document.getElementById('prev').onclick=prev;
  document.getElementById('next').onclick=next;

  // 目錄
  var menu=document.getElementById('menu');
  function buildMenu(){
    var html='<h3>目錄（按 M 或 Esc 關閉）</h3>';
    slides.forEach(function(s,i){
      if(s.dataset.menu){ html+='<a data-i="'+i+'">'+s.dataset.menu+'<small>第 '+(i+1)+' 頁</small></a>'; }
    });
    menu.innerHTML=html;
    [].forEach.call(menu.querySelectorAll('a'),function(a){a.onclick=function(){show(+a.dataset.i);toggleMenu();};});
  }
  function toggleMenu(){menu.classList.toggle('open');}
  document.getElementById('menu-btn').onclick=toggleMenu;

  window.addEventListener('resize',function(){fit();updateMore();}); fit(); buildMenu();
  var h=parseInt((location.hash||'').slice(1),10);
  show(isNaN(h)?0:h-1,false);
})();
