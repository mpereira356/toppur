import React from 'react';
import { useParams, Link } from 'react-router-dom';
import { ArrowLeft, Phone, MessageCircle, CheckCircle, Settings, Wrench } from 'lucide-react';
import { Button } from './ui/button';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';

// Import images
import toppurLogo from '../assets/toppur_logo.jpeg';
import pecasPoliuretano from '../assets/pecas_poliuretano.jpeg';
import pecasBorrachas from '../assets/pecas_borrachas.jpeg';

const ProductDetail = () => {
  const { productId } = useParams();

  const produtos = {
    'mancheta-poliuretano-pu': {
      title: "Mancheta de Poliuretano PU",
      description: "Fabricamos manchetas de poliuretano PU de alta resistência, ideais para aplicações em sistemas hidráulicos e pneumáticos, oferecendo vedação superior e longa vida útil.",
      image: pecasPoliuretano,
      category: "Poliuretano",
      applications: [
        "Sistemas hidráulicos",
        "Sistemas pneumáticos", 
        "Equipamentos industriais",
        "Máquinas pesadas"
      ],
      specifications: {
        "Material": "Poliuretano PU",
        "Dureza": "Shore A 70-95",
        "Temperatura": "-40°C a +80°C",
        "Resistência": "Alta resistência à abrasão",
        "Vedação": "Superior e duradoura"
      },
      benefits: [
        "Vedação superior",
        "Longa vida útil",
        "Alta resistência",
        "Baixa manutenção"
      ]
    },
    'gaxeta-borracha': {
      title: "Gaxeta de Borracha",
      description: "A gaxeta de borracha é essencial para vedação em equipamentos industriais. Nossos modelos são personalizados conforme as necessidades do cliente.",
      image: pecasBorrachas,
      category: "Borracha",
      applications: [
        "Equipamentos industriais",
        "Válvulas e conexões",
        "Sistemas de vedação",
        "Maquinário pesado"
      ],
      specifications: {
        "Material": "Borracha NBR/EPDM",
        "Dureza": "Shore A 60-90",
        "Temperatura": "-30°C a +120°C",
        "Resistência": "Óleos e combustíveis",
        "Personalização": "Sob medida"
      },
      benefits: [
        "Vedação eficiente",
        "Personalização total",
        "Resistente a óleos",
        "Durabilidade comprovada"
      ]
    },
    'coxim-borracha': {
      title: "Coxim de Borracha",
      description: "Os coxims de borracha são usados para absorver vibrações e ruídos em máquinas. Oferecemos modelos sob medida em diversos formatos e durezas.",
      image: pecasBorrachas,
      category: "Borracha",
      applications: [
        "Absorção de vibrações",
        "Redução de ruídos",
        "Isolamento acústico",
        "Suporte de máquinas"
      ],
      specifications: {
        "Material": "Borracha natural/sintética",
        "Dureza": "Shore A 40-80",
        "Temperatura": "-20°C a +80°C",
        "Formatos": "Diversos sob medida",
        "Função": "Anti-vibratório"
      },
      benefits: [
        "Absorve vibrações",
        "Reduz ruídos",
        "Diversos formatos",
        "Sob medida"
      ]
    },
    'revestimento-poliuretano-pu': {
      title: "Revestimento em Poliuretano PU",
      description: "Aplicamos revestimentos em poliuretano PU para proteger peças contra abrasão, impacto e desgaste químico, prolongando a vida útil do equipamento.",
      image: pecasPoliuretano,
      category: "Poliuretano",
      applications: [
        "Proteção contra abrasão",
        "Resistência a impactos",
        "Proteção química",
        "Prolongamento de vida útil"
      ],
      specifications: {
        "Material": "Poliuretano PU",
        "Espessura": "2mm a 50mm",
        "Dureza": "Shore A 60-95",
        "Temperatura": "-40°C a +90°C",
        "Aplicação": "Spray ou moldagem"
      },
      benefits: [
        "Proteção superior",
        "Resistente a químicos",
        "Prolonga vida útil",
        "Aplicação versátil"
      ]
    },
    'bucha-poliuretano-pu': {
      title: "Bucha de Poliuretano PU",
      description: "As buchas de poliuretano PU combinam flexibilidade e resistência, sendo ideais para aplicações mecânicas que exigem alto desempenho.",
      image: pecasPoliuretano,
      category: "Poliuretano",
      applications: [
        "Aplicações mecânicas",
        "Sistemas automotivos",
        "Equipamentos industriais",
        "Máquinas de precisão"
      ],
      specifications: {
        "Material": "Poliuretano PU",
        "Dureza": "Shore A 70-95",
        "Temperatura": "-30°C a +80°C",
        "Características": "Flexível e resistente",
        "Performance": "Alto desempenho"
      },
      benefits: [
        "Flexibilidade",
        "Alta resistência",
        "Alto desempenho",
        "Durabilidade"
      ]
    },
    'ventosa-borracha': {
      title: "Ventosa de Borracha",
      description: "Fabricamos ventosas de borracha com excelente aderência, ideais para sistemas de automação e manipulação de objetos em superfícies lisas.",
      image: pecasBorrachas,
      category: "Borracha",
      applications: [
        "Sistemas de automação",
        "Manipulação de objetos",
        "Superfícies lisas",
        "Equipamentos pneumáticos"
      ],
      specifications: {
        "Material": "Borracha NBR/Silicone",
        "Aderência": "Excelente",
        "Temperatura": "-20°C a +150°C",
        "Superfícies": "Lisas e polidas",
        "Vácuo": "Até -0,8 bar"
      },
      benefits: [
        "Excelente aderência",
        "Para automação",
        "Superfícies lisas",
        "Alta eficiência"
      ]
    }
  };

  const produto = produtos[productId];

  if (!produto) {
    return (
      <div className="min-h-screen bg-white flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-800 mb-4">Produto não encontrado</h1>
          <Link to="/">
            <Button className="btn-toppur">
              <ArrowLeft className="w-4 h-4 mr-2" />
              Voltar ao Início
            </Button>
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-white">
      {/* Header */}
      <header className="bg-white shadow-lg sticky top-0 z-50">
        <div className="container mx-auto px-4">
          {/* Top Bar */}
          <div className="flex justify-between items-center py-2 text-sm border-b">
            <div className="flex space-x-4">
              <a href="tel:+5511991632077" className="flex items-center text-blue-800 hover:text-orange-500 transition-colors">
                <Phone className="w-4 h-4 mr-1" />
                (11) 99163-2077 - Rogerio Laki
              </a>
              <a href="tel:+5511976747658" className="flex items-center text-blue-800 hover:text-orange-500 transition-colors">
                <Phone className="w-4 h-4 mr-1" />
                (11) 97674-7658 - Matheus Medeiros
              </a>
            </div>
          </div>

          {/* Main Navigation */}
          <div className="flex justify-between items-center py-4">
            <Link to="/" className="flex items-center">
              <img src={toppurLogo} alt="TOPPUR Logo" className="h-12 w-auto" />
            </Link>

            <nav className="hidden md:flex space-x-8">
              <Link to="/" className="text-gray-700 hover:text-orange-500 transition-colors font-medium">
                🏠 Início
              </Link>
              <Link to="/#produtos" className="text-gray-700 hover:text-orange-500 transition-colors font-medium">
                🛠 Nossos Produtos
              </Link>
              <Link to="/#sobre" className="text-gray-700 hover:text-orange-500 transition-colors font-medium">
                📄 Sobre
              </Link>
              <Link to="/#contato" className="text-gray-700 hover:text-orange-500 transition-colors font-medium">
                📞 Contato
              </Link>
            </nav>
          </div>
        </div>
      </header>

      {/* Breadcrumb */}
      <div className="bg-gray-50 py-4">
        <div className="container mx-auto px-4">
          <div className="flex items-center space-x-2 text-sm text-gray-600">
            <Link to="/" className="hover:text-orange-500">Início</Link>
            <span>/</span>
            <Link to="/#produtos" className="hover:text-orange-500">Produtos</Link>
            <span>/</span>
            <span className="text-gray-800">{produto.title}</span>
          </div>
        </div>
      </div>

      {/* Product Detail */}
      <div className="container mx-auto px-4 py-12">
        <div className="grid lg:grid-cols-2 gap-12">
          {/* Product Image */}
          <div className="space-y-4">
            <div className="aspect-square overflow-hidden rounded-lg bg-gray-100">
              <img 
                src={produto.image} 
                alt={produto.title}
                className="w-full h-full object-cover"
              />
            </div>
          </div>

          {/* Product Info */}
          <div className="space-y-6">
            <div>
              <Badge variant="secondary" className="mb-4">
                {produto.category}
              </Badge>
              <h1 className="text-4xl font-bold text-gray-800 mb-4">
                {produto.title}
              </h1>
              <p className="text-xl text-gray-600 leading-relaxed">
                {produto.description}
              </p>
            </div>

            {/* Benefits */}
            <div>
              <h3 className="text-xl font-semibold text-gray-800 mb-4">Principais Benefícios</h3>
              <div className="grid grid-cols-2 gap-3">
                {produto.benefits.map((benefit, index) => (
                  <div key={index} className="flex items-center space-x-2">
                    <CheckCircle className="w-5 h-5 text-green-500" />
                    <span className="text-gray-700">{benefit}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row gap-4">
              <a
                href="https://wa.me/5511991632077"
                target="_blank"
                rel="noopener noreferrer"
                className="flex-1"
              >
                <Button className="w-full btn-toppur">
                  <MessageCircle className="w-4 h-4 mr-2" />
                  Solicitar Orçamento
                </Button>
              </a>
              <a href="tel:+5511991632077" className="flex-1">
                <Button variant="outline" className="w-full">
                  <Phone className="w-4 h-4 mr-2" />
                  Ligar Agora
                </Button>
              </a>
            </div>
          </div>
        </div>

        {/* Specifications and Applications */}
        <div className="grid lg:grid-cols-2 gap-8 mt-16">
          {/* Specifications */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Settings className="w-5 h-5 mr-2 text-orange-500" />
                Especificações Técnicas
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {Object.entries(produto.specifications).map(([key, value]) => (
                  <div key={key} className="flex justify-between py-2 border-b border-gray-100 last:border-b-0">
                    <span className="font-medium text-gray-700">{key}:</span>
                    <span className="text-gray-600">{value}</span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Applications */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Wrench className="w-5 h-5 mr-2 text-orange-500" />
                Aplicações
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {produto.applications.map((application, index) => (
                  <div key={index} className="flex items-center space-x-3">
                    <div className="w-2 h-2 bg-orange-500 rounded-full"></div>
                    <span className="text-gray-700">{application}</span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Back Button */}
        <div className="mt-12 text-center">
          <Link to="/">
            <Button variant="outline" className="px-8">
              <ArrowLeft className="w-4 h-4 mr-2" />
              Voltar aos Produtos
            </Button>
          </Link>
        </div>
      </div>

      {/* WhatsApp Float Button */}
      <a
        href="https://wa.me/5511991632077"
        target="_blank"
        rel="noopener noreferrer"
        className="whatsapp-float flex items-center justify-center"
        title="Fale conosco no WhatsApp"
      >
        <MessageCircle className="w-8 h-8" />
      </a>
    </div>
  );
};

export default ProductDetail;

