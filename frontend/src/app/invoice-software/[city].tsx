import { Metadata } from 'next';
import { notFound } from 'next/navigation';

// Define the props for the page
type Props = {
  params: { city: string };
};

// Generate the metadata for the page
export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const city = params.city.charAt(0).toUpperCase() + params.city.slice(1);
  return {
    title: `Invoice Management Software ${city} | GST & AI | TrulyInvoice`,
    description: `#1 Invoice software in ${city}. AI-powered GST invoicing, automatic data extraction, 1-click exports. Trusted by 5000+ ${city} businesses. Try Free!`,
    alternates: {
      canonical: `https://trulyinvoice.xyz/invoice-software-${params.city}`,
    },
  };
}

// Define the page component
export default function CityPage({ params }: Props) {
  const city = params.city.charAt(0).toUpperCase() + params.city.slice(1);

  // You can fetch city-specific data here
  // For now, we'll just display the city name

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-4xl font-bold mb-4">
        Best Invoice Management Software for {city} Businesses
      </h1>
      <p className="text-lg">
        This is a placeholder page for {city}. You can add city-specific content here.
      </p>
    </div>
  );
}
