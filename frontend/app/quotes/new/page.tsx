'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';

interface QuoteFormData {
  consumer_name: string;
  consumer_email: string;
  consumer_phone: string;
  coverage_type: string;
  coverage_amount: string;
  coverage_start_date: string;
  coverage_details: Record<string, unknown>;
}

export default function NewQuotePage() {
  const router = useRouter();
  const [error, setError] = useState<string>('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setLoading(true);
    setError('');

    const formData = new FormData(event.currentTarget);
    const quoteData: QuoteFormData = {
      consumer_name: formData.get('consumer_name') as string,
      consumer_email: formData.get('consumer_email') as string,
      consumer_phone: formData.get('consumer_phone') as string,
      coverage_type: formData.get('coverage_type') as string,
      coverage_amount: formData.get('coverage_amount') as string,
      coverage_start_date: formData.get('coverage_start_date') as string,
      coverage_details: {},
    };

    try {
      const response = await fetch('http://localhost:8000/api/marketplace/quotes', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(quoteData),
      });

      if (!response.ok) {
        throw new Error('Failed to submit quote');
      }

      const result = await response.json();
      router.push(`/quotes/${result.id}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 py-8">
      <div className="max-w-2xl mx-auto px-4">
        <h1 className="text-3xl font-bold mb-8 text-white text-center">
          Request Insurance Quote
        </h1>

        {error && (
          <div className="bg-red-900/50 border border-red-500 text-red-200 px-4 py-3 rounded-lg mb-6">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6 bg-gray-800 rounded-xl p-6 shadow-xl">
          <div>
            <label htmlFor="consumer_name" className="block text-sm font-medium text-gray-200 mb-1">
              Full Name
            </label>
            <input
              type="text"
              name="consumer_name"
              id="consumer_name"
              required
              className="mt-1 block w-full rounded-lg bg-gray-700 border-gray-600 text-white
                       shadow-sm focus:border-blue-500 focus:ring-blue-500
                       placeholder-gray-400"
              placeholder="John Doe"
            />
          </div>

          <div>
            <label htmlFor="consumer_email" className="block text-sm font-medium text-gray-200 mb-1">
              Email
            </label>
            <input
              type="email"
              name="consumer_email"
              id="consumer_email"
              required
              className="mt-1 block w-full rounded-lg bg-gray-700 border-gray-600 text-white
                       shadow-sm focus:border-blue-500 focus:ring-blue-500
                       placeholder-gray-400"
              placeholder="john@example.com"
            />
          </div>

          <div>
            <label htmlFor="consumer_phone" className="block text-sm font-medium text-gray-200 mb-1">
              Phone Number
            </label>
            <input
              type="tel"
              name="consumer_phone"
              id="consumer_phone"
              required
              className="mt-1 block w-full rounded-lg bg-gray-700 border-gray-600 text-white
                       shadow-sm focus:border-blue-500 focus:ring-blue-500
                       placeholder-gray-400"
              placeholder="(555) 555-5555"
            />
          </div>

          <div>
            <label htmlFor="coverage_type" className="block text-sm font-medium text-gray-200 mb-1">
              Coverage Type
            </label>
            <select
              name="coverage_type"
              id="coverage_type"
              required
              className="mt-1 block w-full rounded-lg bg-gray-700 border-gray-600 text-white
                       shadow-sm focus:border-blue-500 focus:ring-blue-500"
            >
              <option value="" className="text-gray-400">Select coverage type</option>
              <option value="auto">Auto Insurance</option>
              <option value="home">Home Insurance</option>
              <option value="life">Life Insurance</option>
              <option value="health">Health Insurance</option>
            </select>
          </div>

          <div>
            <label htmlFor="coverage_amount" className="block text-sm font-medium text-gray-200 mb-1">
              Coverage Amount ($)
            </label>
            <input
              type="number"
              name="coverage_amount"
              id="coverage_amount"
              required
              min="1000"
              step="1000"
              className="mt-1 block w-full rounded-lg bg-gray-700 border-gray-600 text-white
                       shadow-sm focus:border-blue-500 focus:ring-blue-500
                       placeholder-gray-400"
              placeholder="50000"
            />
          </div>

          <div>
            <label htmlFor="coverage_start_date" className="block text-sm font-medium text-gray-200 mb-1">
              Coverage Start Date
            </label>
            <input
              type="date"
              name="coverage_start_date"
              id="coverage_start_date"
              required
              min={new Date().toISOString().split('T')[0]}
              className="mt-1 block w-full rounded-lg bg-gray-700 border-gray-600 text-white
                       shadow-sm focus:border-blue-500 focus:ring-blue-500"
            />
          </div>

          <div className="pt-4">
            <button
              type="submit"
              disabled={loading}
              className="w-full flex justify-center py-3 px-4 border border-transparent rounded-lg
                       text-sm font-medium text-white bg-blue-600 hover:bg-blue-700
                       focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500
                       disabled:opacity-50 disabled:cursor-not-allowed
                       transition-colors duration-200
                       shadow-lg"
            >
              {loading ? 'Submitting...' : 'Submit Quote Request'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
