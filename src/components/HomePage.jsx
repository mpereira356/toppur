import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Phone, Factory, Shield, Clock, Award, Menu, X, MessageCircle } from 'lucide-react';
import { Button } from './ui/button';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Input } from './ui/input';
import { Textarea } from './ui/textarea';

// Import images
import toppurLogo from '../assets/toppur_logo.jpeg';
import pecasPoliuretano from '../assets/pecas_poliuretano.jpeg';
import pecasBorrachas from '../assets/pecas_borrachas.jpeg';

const HomePage = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [formData, setFormData] = useState({
    nome: '',
    sobrenome: '',
    telefone: '',
    email: '',
    mensagem: ''
  });

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Formulário enviado:', formData);
    alert('Mensagem enviada com sucesso! Entraremos em contato em breve.');
    setFormData({
      nome: '',
      sobrenome: '',
      telefone: '',
      email: '',
      mensagem: ''
    });
  };

  const scrollToSection = (sectionId) => {
    document.getElementById(sectionId)?.scrollIntoView({ behavior: 'smooth' });
    setIsMenuOpen(false);
  };

  const produtos = [
    {
      id: 'mancheta-poliuretano-pu',
      title: "Mancheta de Poliuretano PU",
      description: "Fabricamos manchetas de poliuretano PU de alta resistência, ideais para aplicações em sistemas hidráulicos e pneumáticos, oferecendo vedação superior e longa vida útil.",
      image: pecasPoliuretano
    },
    {
      id: 'gaxeta-borracha',
      title: "Gaxeta de Borracha",
      description: "A gaxeta de borracha é essencial para vedação em equipamentos industriais. Nossos modelos são personalizados conforme as necessidades do cliente.",
      image: pecasBorrachas
    },
    {
      id: 'coxim-borracha',
      title: "Coxim de Borracha",
      description: "Os coxims de borracha são usados para absorver vibrações e ruídos em máquinas. Oferecemos modelos sob medida em diversos formatos e durezas.",
      image: pecasBorrachas
    },
    {
      id: 'revestimento-poliuretano-pu',
      title: "Revestimento em Poliuretano PU",
      description: "Aplicamos revestimentos em poliuretano PU para proteger peças contra abrasão, impacto e desgaste químico, prolongando a vida útil do equipamento.",
      image: pecasPoliuretano
    },
    {
      id: 'bucha-poliuretano-pu',
      title: "Bucha de Poliuretano PU",
      description: "As buchas de poliuretano PU combinam flexibilidade e resistência, sendo ideais para aplicações mecânicas que exigem alto desempenho.",
      image: pecasPoliuretano
    },
    {
      id: 'ventosa-borracha',
      title: "Ventosa de Borracha",
      description: "Fabricamos ventosas de borracha com excelente aderência, ideais para sistemas de automação e manipulação de objetos em superfícies lisas.",
      image: pecasBorrachas
    }
  ];

  const diferenciais = [
    {
      icon: <Factory className="w-8 h-8 text-orange-500" />,
      title: "Fabricação Própria",
      description: "Produção sob medida com controle total de qualidade"
    },
    {
      icon: <Shield className="w-8 h-8 text-orange-500" />,
      title: "Alta Qualidade",
      description: "Materiais premium e processos certificados"
    },
    {
      icon: <Clock className="w-8 h-8 text-orange-500" />,
      title: "Entrega Rápida",
      description: "Prazos otimizados para atender suas necessidades"
    },
    {
      icon: <Award className="w-8 h-8 text-orange-500" />,
      title: "Experiência",
      description: "Anos de expertise em soluções industriais"
    }
  ];

  return (
    <div className="min-h-screen bg-white scroll-smooth">
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
            <div className="flex items-center">
              <img src={toppurLogo} alt="TOPPUR Logo" className="h-12 w-auto" />
            </div>

            {/* Desktop Navigation */}
            <nav className="hidden md:flex space-x-8">
              <button onClick={() => scrollToSection('inicio')} className="text-gray-700 hover:text-orange-500 transition-colors font-medium">
                🏠 Início
              </button>
              <button onClick={() => scrollToSection('produtos')} className="text-gray-700 hover:text-orange-500 transition-colors font-medium">
                🛠 Nossos Produtos
              </button>
              <button onClick={() => scrollToSection('sobre')} className="text-gray-700 hover:text-orange-500 transition-colors font-medium">
                📄 Sobre
              </button>
              <button onClick={() => scrollToSection('contato')} className="text-gray-700 hover:text-orange-500 transition-colors font-medium">
                📞 Contato
              </button>
            </nav>

            {/* Mobile Menu Button */}
            <button 
              className="md:hidden"
              onClick={() => setIsMenuOpen(!isMenuOpen)}
            >
              {isMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>

          {/* Mobile Navigation */}
          {isMenuOpen && (
            <nav className="md:hidden py-4 border-t">
              <div className="flex flex-col space-y-4">
                <button onClick={() => scrollToSection('inicio')} className="text-left text-gray-700 hover:text-orange-500 transition-colors font-medium">
                  🏠 Início
                </button>
                <button onClick={() => scrollToSection('produtos')} className="text-left text-gray-700 hover:text-orange-500 transition-colors font-medium">
                  🛠 Nossos Produtos
                </button>
                <button onClick={() => scrollToSection('sobre')} className="text-left text-gray-700 hover:text-orange-500 transition-colors font-medium">
                  📄 Sobre
                </button>
                <button onClick={() => scrollToSection('contato')} className="text-left text-gray-700 hover:text-orange-500 transition-colors font-medium">
                  📞 Contato
                </button>
              </div>
            </nav>
          )}
        </div>
      </header>

      {/* Hero Section */}
      <section id="inicio" className="toppur-hero-bg min-h-screen flex items-center">
        <div className="container mx-auto px-4 text-center text-white">
          <div className="max-w-4xl mx-auto fade-in">
            <h1 className="text-5xl md:text-7xl font-bold mb-6">
              TOPPUR
            </h1>
            <h2 className="text-2xl md:text-4xl font-semibold mb-8">
              Poliuretano e Borracha
            </h2>
            <p className="text-xl md:text-2xl mb-12 leading-relaxed">
              Peças técnicas industriais de alta qualidade em borracha, poliuretano e plásticos industriais sob medida
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button 
                onClick={() => scrollToSection('produtos')} 
                className="btn-toppur px-8 py-4 text-lg font-semibold"
              >
                Conheça Nossos Produtos
              </Button>
              <Button 
                onClick={() => scrollToSection('contato')} 
                variant="outline" 
                className="px-8 py-4 text-lg font-semibold bg-white/10 border-white text-white hover:bg-white hover:text-blue-800"
              >
                Entre em Contato
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Diferenciais */}
      <section className="py-20 bg-gray-50">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-800 mb-4 section-title">
              Por que escolher a TOPPUR?
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Já pensou em comprar direto da fábrica? Oferecemos o melhor equilíbrio entre qualidade, custo-benefício e pontualidade nas entregas.
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {diferenciais.map((item, index) => (
              <Card key={index} className="text-center product-card bg-white">
                <CardHeader>
                  <div className="flex justify-center mb-4">
                    {item.icon}
                  </div>
                  <CardTitle className="text-xl font-semibold text-gray-800">
                    {item.title}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-gray-600">{item.description}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Produtos */}
      <section id="produtos" className="py-20">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-800 mb-4 section-title">
              🛠️ Conheça Nossos Produtos
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Oferecemos uma ampla variedade de produtos em borracha e poliuretano, ideais para aplicações industriais, automotivas e diversas outras áreas.
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {produtos.map((produto, index) => (
              <Card key={index} className="product-card overflow-hidden">
                <div className="h-48 overflow-hidden">
                  <img 
                    src={produto.image} 
                    alt={produto.title}
                    className="w-full h-full object-cover transition-transform duration-300 hover:scale-110"
                  />
                </div>
                <CardHeader>
                  <CardTitle className="text-xl font-semibold text-gray-800">
                    {produto.title}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-gray-600 leading-relaxed mb-4">
                    {produto.description}
                  </p>
                  <Link to={`/produto/${produto.id}`}>
                    <Button className="w-full btn-toppur">
                      Ver Detalhes
                    </Button>
                  </Link>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Sobre */}
      <section id="sobre" className="py-20 bg-gray-50">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-800 mb-4 section-title">
              Sobre a TOPPUR
            </h2>
          </div>

          <div className="grid lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
            <Card className="product-card">
              <CardHeader>
                <div className="text-center mb-4">
                  <div className="w-16 h-16 bg-orange-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <span className="text-2xl">🎯</span>
                  </div>
                  <CardTitle className="text-2xl font-bold text-gray-800">
                    Nosso Objetivo
                  </CardTitle>
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-gray-600 leading-relaxed">
                  Na TOPPUR, buscamos alcançar a plena satisfação de nossos clientes, oferecendo o melhor equilíbrio entre qualidade, custo-benefício e pontualidade nas entregas. Colocamos os interesses e as necessidades técnicas dos nossos clientes em primeiro lugar.
                </p>
              </CardContent>
            </Card>

            <Card className="product-card">
              <CardHeader>
                <div className="text-center mb-4">
                  <div className="w-16 h-16 bg-orange-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <span className="text-2xl">🚀</span>
                  </div>
                  <CardTitle className="text-2xl font-bold text-gray-800">
                    Nossa Missão
                  </CardTitle>
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-gray-600 leading-relaxed">
                  Atender com excelência as demandas do mercado, fornecendo peças técnicas em poliuretano, borracha e plásticos industriais. Valorizamos a inovação, a eficiência e a sustentabilidade em cada etapa do nosso processo.
                </p>
              </CardContent>
            </Card>

            <Card className="product-card">
              <CardHeader>
                <div className="text-center mb-4">
                  <div className="w-16 h-16 bg-orange-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <span className="text-2xl">👁️</span>
                  </div>
                  <CardTitle className="text-2xl font-bold text-gray-800">
                    Nossa Visão
                  </CardTitle>
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-gray-600 leading-relaxed">
                  Ser reconhecida como referência nacional em atendimento técnico especializado, destacando-se pela qualidade, agilidade e compromisso no fornecimento de peças técnicas de alto desempenho.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Contato */}
      <section id="contato" className="py-20">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-800 mb-4 section-title">
              🔩 Entre em Contato
            </h2>
            <p className="text-xl text-gray-600">
              Sempre prontos para te atender! Entre em contato conosco.
            </p>
          </div>

          <div className="max-w-4xl mx-auto">
            <Card className="contact-form">
              <CardContent className="p-8">
                <form onSubmit={handleSubmit} className="space-y-6">
                  <div className="grid md:grid-cols-2 gap-6">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Nome *
                      </label>
                      <Input
                        type="text"
                        name="nome"
                        value={formData.nome}
                        onChange={handleInputChange}
                        required
                        className="w-full"
                        placeholder="Seu nome"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Sobrenome
                      </label>
                      <Input
                        type="text"
                        name="sobrenome"
                        value={formData.sobrenome}
                        onChange={handleInputChange}
                        className="w-full"
                        placeholder="Seu sobrenome"
                      />
                    </div>
                  </div>

                  <div className="grid md:grid-cols-2 gap-6">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Telefone *
                      </label>
                      <Input
                        type="tel"
                        name="telefone"
                        value={formData.telefone}
                        onChange={handleInputChange}
                        required
                        className="w-full"
                        placeholder="(11) 99999-9999"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        E-mail
                      </label>
                      <Input
                        type="email"
                        name="email"
                        value={formData.email}
                        onChange={handleInputChange}
                        className="w-full"
                        placeholder="seu@email.com"
                      />
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Comentário ou Mensagem *
                    </label>
                    <Textarea
                      name="mensagem"
                      value={formData.mensagem}
                      onChange={handleInputChange}
                      required
                      rows={5}
                      className="w-full"
                      placeholder="Descreva sua necessidade ou dúvida..."
                    />
                  </div>

                  <div className="text-center">
                    <Button type="submit" className="btn-toppur px-12 py-3 text-lg font-semibold">
                      Enviar Mensagem
                    </Button>
                  </div>
                </form>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-800 text-white py-12">
        <div className="container mx-auto px-4">
          <div className="grid md:grid-cols-3 gap-8">
            <div>
              <img src={toppurLogo} alt="TOPPUR Logo" className="h-12 w-auto mb-4 filter brightness-0 invert" />
              <p className="text-gray-300 leading-relaxed">
                Especialistas em peças técnicas industriais em borracha, poliuretano e plásticos industriais sob medida.
              </p>
            </div>
            
            <div>
              <h3 className="text-xl font-semibold mb-4">Contato</h3>
              <div className="space-y-2">
                <a href="tel:+5511991632077" className="flex items-center text-gray-300 hover:text-orange-500 transition-colors">
                  <Phone className="w-4 h-4 mr-2" />
                  (11) 99163-2077 - Rogerio Laki
                </a>
                <a href="tel:+5511976747658" className="flex items-center text-gray-300 hover:text-orange-500 transition-colors">
                  <Phone className="w-4 h-4 mr-2" />
                  (11) 97674-7658 - Matheus Medeiros
                </a>
              </div>
            </div>

            <div>
              <h3 className="text-xl font-semibold mb-4">Navegação</h3>
              <div className="space-y-2">
                <button onClick={() => scrollToSection('inicio')} className="block text-gray-300 hover:text-orange-500 transition-colors">
                  Início
                </button>
                <button onClick={() => scrollToSection('produtos')} className="block text-gray-300 hover:text-orange-500 transition-colors">
                  Nossos Produtos
                </button>
                <button onClick={() => scrollToSection('sobre')} className="block text-gray-300 hover:text-orange-500 transition-colors">
                  Sobre
                </button>
                <button onClick={() => scrollToSection('contato')} className="block text-gray-300 hover:text-orange-500 transition-colors">
                  Contato
                </button>
              </div>
            </div>
          </div>

          <div className="border-t border-gray-700 mt-8 pt-8 text-center">
            <p className="text-gray-400">
              © 2024 TOPPUR Poliuretano e Borracha. Todos os direitos reservados.
            </p>
          </div>
        </div>
      </footer>

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

export default HomePage;

