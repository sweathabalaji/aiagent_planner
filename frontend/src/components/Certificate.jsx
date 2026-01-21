import { useState } from 'react';
import { TrophyIcon, AcademicCapIcon, CalendarIcon, ClockIcon, StarIcon } from '@heroicons/react/24/solid';

export default function Certificate({ sessionId, assessmentScore }) {
  const [certificate, setCertificate] = useState(null);
  const [userName, setUserName] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [showNameInput, setShowNameInput] = useState(true);

  const generateCertificate = async () => {
    if (!userName.trim()) {
      alert('Please enter your name');
      return;
    }

    setIsLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/learning/generate-certificate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          session_id: sessionId,
          user_name: userName.trim()
        }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to generate certificate');
      }

      const data = await response.json();
      setCertificate(data.certificate);
      setShowNameInput(false);
    } catch (error) {
      console.error('Error generating certificate:', error);
      alert(error.message || 'Failed to generate certificate. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handlePrint = () => {
    window.print();
  };

  if (showNameInput && !certificate) {
    return (
      <div className="bg-white rounded-lg shadow-md p-8 text-center">
        <TrophyIcon className="w-20 h-20 text-yellow-500 mx-auto mb-4" />
        <h2 className="text-3xl font-bold text-gray-900 mb-4">
          Generate Your Certificate! 🎉
        </h2>
        <p className="text-gray-600 mb-6">
          Congratulations on passing the assessment! Enter your name to receive your completion certificate.
        </p>
        
        <div className="max-w-md mx-auto">
          <input
            type="text"
            value={userName}
            onChange={(e) => setUserName(e.target.value)}
            placeholder="Enter your full name"
            className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg mb-4 focus:outline-none focus:border-purple-600 text-center text-lg"
            onKeyPress={(e) => e.key === 'Enter' && generateCertificate()}
          />
          <button
            onClick={generateCertificate}
            disabled={isLoading || !userName.trim()}
            className="bg-gradient-to-r from-purple-600 to-blue-600 text-white px-8 py-3 rounded-lg font-semibold hover:from-purple-700 hover:to-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all transform hover:scale-105 w-full"
          >
            {isLoading ? 'Generating...' : 'Generate Certificate'}
          </button>
        </div>
      </div>
    );
  }

  if (!certificate) return null;

  return (
    <div className="space-y-6">
      {/* Print Button */}
      <div className="text-center no-print">
        <button
          onClick={handlePrint}
          className="bg-blue-600 text-white px-6 py-2 rounded-lg font-semibold hover:bg-blue-700 transition-all"
        >
          🖨️ Print Certificate
        </button>
      </div>

      {/* Certificate */}
      <div className="bg-white rounded-lg shadow-2xl p-4 md:p-6 certificate-container">
        {/* Decorative Border */}
        <div className="border-4 border-double border-purple-600 rounded-lg p-4 md:p-6 relative">
          {/* Corner Decorations */}
          <div className="absolute top-2 left-2 w-8 h-8 border-t-2 border-l-2 border-yellow-500"></div>
          <div className="absolute top-2 right-2 w-8 h-8 border-t-2 border-r-2 border-yellow-500"></div>
          <div className="absolute bottom-2 left-2 w-8 h-8 border-b-2 border-l-2 border-yellow-500"></div>
          <div className="absolute bottom-2 right-2 w-8 h-8 border-b-2 border-r-2 border-yellow-500"></div>

          {/* Header */}
          <div className="text-center mb-4">
            <div className="flex items-center justify-center gap-2 mb-2">
              <AcademicCapIcon className="w-10 h-10 text-purple-600" />
              <TrophyIcon className="w-10 h-10 text-yellow-500" />
            </div>
            <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-1" style={{ fontFamily: 'Georgia, serif' }}>
              Certificate of Completion
            </h1>
            <div className="flex items-center justify-center gap-1 text-yellow-600">
              <StarIcon className="w-4 h-4" />
              <StarIcon className="w-4 h-4" />
              <StarIcon className="w-4 h-4" />
            </div>
          </div>

          {/* Content */}
          <div className="text-center space-y-3">
            <p className="text-base text-gray-700">This is to certify that</p>
            
            <div className="py-2 border-b-2 border-gray-300">
              <p className="text-2xl md:text-3xl font-bold text-purple-700" style={{ fontFamily: 'Georgia, serif' }}>
                {certificate.recipient_name}
              </p>
            </div>

            <p className="text-base text-gray-700">has successfully completed</p>

            <div className="bg-gradient-to-r from-purple-50 to-blue-50 rounded-lg p-3 border-2 border-purple-200">
              <h2 className="text-xl md:text-2xl font-bold text-gray-900 mb-1">
                {certificate.course_title}
              </h2>
              <p className="text-sm text-gray-600">with distinction</p>
            </div>

            {/* Details Grid */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-2 mt-4">
              <div className="bg-gray-50 rounded-lg p-2">
                <div className="flex items-center justify-center gap-1 text-purple-600 mb-1">
                  <CalendarIcon className="w-4 h-4" />
                  <span className="font-semibold text-xs">Completion Date</span>
                </div>
                <p className="text-gray-900 font-medium text-sm">{certificate.completion_date}</p>
              </div>

              <div className="bg-gray-50 rounded-lg p-2">
                <div className="flex items-center justify-center gap-1 text-blue-600 mb-1">
                  <ClockIcon className="w-4 h-4" />
                  <span className="font-semibold text-xs">Total Hours</span>
                </div>
                <p className="text-gray-900 font-medium text-sm">{certificate.total_hours} hours</p>
              </div>

              <div className="bg-gray-50 rounded-lg p-2">
                <div className="flex items-center justify-center gap-1 text-green-600 mb-1">
                  <TrophyIcon className="w-4 h-4" />
                  <span className="font-semibold text-xs">Assessment Score</span>
                </div>
                <p className="text-gray-900 font-medium text-sm">{certificate.assessment_score.toFixed(1)}%</p>
              </div>
            </div>

            {/* Skills Acquired */}
            {certificate.skills_acquired && certificate.skills_acquired.length > 0 && (
              <div className="mt-4">
                <h3 className="text-sm font-semibold text-gray-900 mb-2">Skills Acquired</h3>
                <div className="flex flex-wrap gap-1 justify-center">
                  {certificate.skills_acquired.slice(0, 6).map((skill, index) => (
                    <span
                      key={index}
                      className="bg-purple-100 text-purple-700 px-2 py-1 rounded-full text-xs font-medium border border-purple-300"
                    >
                      {skill}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Footer */}
            <div className="mt-6 pt-4 border-t-2 border-gray-200">
              <div className="flex flex-col md:flex-row justify-between items-center gap-3">
                <div className="text-center md:text-left">
                  <div className="border-t-2 border-gray-900 pt-1 mb-1 w-40 mx-auto md:mx-0">
                    <p className="font-semibold text-gray-900 text-sm">Authorized Signature</p>
                  </div>
                  <p className="text-xs text-gray-600">{certificate.issued_by}</p>
                </div>

                <div className="text-center">
                  <div className="bg-gray-100 border-2 border-gray-300 rounded-lg p-2">
                    <p className="text-xs text-gray-600 font-mono">Certificate ID</p>
                    <p className="text-xs font-bold text-gray-900 font-mono">
                      {certificate.certificate_id}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Additional Info */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 text-center no-print">
        <p className="text-blue-900 font-semibold">
          🎓 Save this certificate for your portfolio and professional profiles!
        </p>
      </div>
    </div>
  );
}
