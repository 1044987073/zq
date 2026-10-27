export type Product = {
  id: string;
  name: string;
  price: number;
  priceLabel: string;
  cost: number;
  stock: number | null;
  enabled: boolean;
  tag: string;
  duration: string;
  age: string;
  cover: string;
  steps: string[];
  desc: string;
};

export const defaultProducts: Product[] = [
  {
    id: 'mask',
    name: 'DIY 面具绘画',
    price: 15,
    priceLabel: '15 元/个',
    cost: 2.1,
    stock: 10,
    enabled: true,
    tag: '热门',
    duration: '约 15 分钟',
    age: '4–10 岁',
    cover: '',
    steps: ['选空白面具', '丙烯自由涂色', '现场晾干带走'],
    desc: '可加羽毛贴纸提价，适合低龄小朋友。'
  },
  {
    id: 'pumpkin-s',
    name: '南瓜石膏娃娃（小）',
    price: 10,
    priceLabel: '10–12 元/个',
    cost: 2.8,
    stock: 15,
    enabled: true,
    tag: '招牌',
    duration: '约 20 分钟',
    age: '5 岁+',
    cover: '',
    steps: ['小锤敲开石膏壳', '取出南瓜娃娃', '涂色装饰带走'],
    desc: '「砸」的过程很解压，围观引流效果好。'
  },
  {
    id: 'fan',
    name: '涂鸦扇子',
    price: 8,
    priceLabel: '8–10 元/把',
    cost: 0.34,
    stock: 20,
    enabled: true,
    tag: '走量',
    duration: '约 10 分钟',
    age: '全年龄',
    cover: '',
    steps: ['选空白扇面', '现场绘画', '即取即用'],
    desc: '成本低、周转快。'
  },
  {
    id: 'wish-55',
    name: '许愿瓶 55ml',
    price: 15,
    priceLabel: '15–20 元/个',
    cost: 1.34,
    stock: 10,
    enabled: true,
    tag: '推荐',
    duration: '约 15 分钟',
    age: '6 岁+',
    cover: '',
    steps: ['大瓶更多装饰', '泡大珠变色', '许愿带走'],
    desc: '提醒 3 岁以下勿误吞小珠。'
  }
];

export const defaultBundles = [
  { id: 'a', name: '小朋友套餐 A', price: 48, items: ['面具', '小石膏', '小许愿瓶'] },
  { id: 'b', name: '体验套餐 B', price: 58, items: ['大石膏', '考古', '大许愿瓶'] }
];
