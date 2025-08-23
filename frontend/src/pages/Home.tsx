import MedicalDisclaimer from "../components/MedicalDisclaimer";
import Navbar from "../components/Navbar";
import HeroSection from "../components/HeroSection";
import FeaturesGrid from "../components/FeaturesGrid";
import TestimonialCards from "../components/TestimonialCards";
import Footer from "../components/Footer";

export default function Home() {
  return (
    <>
      <MedicalDisclaimer />
      <Navbar />
      <main>
        <HeroSection />
        <FeaturesGrid />
        <TestimonialCards />
      </main>
      <Footer />
    </>
  );
}
