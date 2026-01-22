// Sample product data (could be fetched from server)
const PRODUCTS = [
  {id:1, name:'Classic Sneakers', price:59.99, img:'/static/assets/images/sneakers.jpg'},
  {id:2, name:'Leather Jacket', price:129.99, img:'/static/assets/images/leather-jacket.jpg'},
  {id:3, name:'Smart Watch', price:199.99, img:'/static/assets/images/smart-watch.jpg'},
  {id:4, name:'Denim Jeans', price:49.99, img:'/static/assets/images/denim-jeans.jpg'},
  {id:5, name:'Sunglasses', price:19.99, img:'/static/assets/images/sunglasses.jpg'},
  {id:6, name:'Backpack', price:39.99, img:'/static/assets/images/backpack.jpg'}
];

const $ = selector => document.querySelector(selector);
const $$ = selector => Array.from(document.querySelectorAll(selector));

function save(key, value){ localStorage.setItem(key, JSON.stringify(value)); }
function load(key){ const v = localStorage.getItem(key); return v ? JSON.parse(v) : []; }






function initSearch(){
  const input = $('#searchInput');
  const btn = $('#searchBtn');
  function doSearch(){
    const q = input.value.trim().toLowerCase();
    if(!q) return renderProducts(PRODUCTS);
    const filtered = PRODUCTS.filter(p=>p.name.toLowerCase().includes(q));
    renderProducts(filtered);
  }
  btn.addEventListener('click', doSearch);
  input.addEventListener('keydown', e=>{ if(e.key==='Enter') doSearch(); });
}



document.addEventListener('DOMContentLoaded', init);
function changeMainImage(thumbnail) {
    // Update main image
    const mainImage = document.getElementById('mainImage');
    mainImage.src = thumbnail.src;
    
    // Update active thumbnail
    document.querySelectorAll('.thumbnail').forEach(t => t.classList.remove('active'));
    thumbnail.classList.add('active');
}
