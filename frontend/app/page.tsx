"use client";

import { ChangeEvent, DragEvent, useRef, useState } from "react";

export default function Home() {
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [error, setError] = useState("");
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const validateAndSetImage = (file: File) => {
    setError("");

    const allowedTypes = ["image/jpeg", "image/jpg", "image/png"];

    if (!allowedTypes.includes(file.type)) {
      setError("Please upload a JPG, JPEG, or PNG image.");
      return;
    }

    if (file.size > 10 * 1024 * 1024) {
      setError("Image size must be less than 10 MB.");
      return;
    }

    setSelectedImage(file);

    const imageUrl = URL.createObjectURL(file);
    setPreview(imageUrl);
  };

  const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];

    if (file) {
      validateAndSetImage(file);
    }
  };

  const handleDrop = (event: DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    setIsDragging(false);

    const file = event.dataTransfer.files?.[0];

    if (file) {
      validateAndSetImage(file);
    }
  };

  const removeImage = () => {
    setSelectedImage(null);
    setPreview(null);
    setError("");

    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  return (
    <main className="min-h-screen bg-[#f7faf5] text-slate-900">
      {/* Navigation */}
      <nav className="border-b border-green-100 bg-white/90 backdrop-blur">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-green-600 text-xl text-white">
              🌱
            </div>

            <div>
              <h1 className="text-xl font-bold tracking-tight text-green-800">
                Crop Care
              </h1>
              <p className="text-xs text-slate-500">Smart crop protection</p>
            </div>
          </div>

          <div className="hidden items-center gap-8 text-sm font-medium md:flex">
            <a href="#" className="text-green-700">
              Home
            </a>
            <a href="#detect" className="text-slate-600 hover:text-green-700">
              Disease Detection
            </a>
            <a href="#about" className="text-slate-600 hover:text-green-700">
              About
            </a>
          </div>

          <button className="rounded-lg border border-green-200 px-4 py-2 text-sm font-semibold text-green-700 hover:bg-green-50">
            Farmer Login
          </button>
        </div>
      </nav>

      {/* Hero */}
      <section className="mx-auto grid max-w-7xl items-center gap-12 px-6 py-16 lg:grid-cols-2 lg:py-24">
        <div>
          <div className="mb-5 inline-flex items-center gap-2 rounded-full bg-green-100 px-4 py-2 text-sm font-semibold text-green-800">
            <span>🌿</span>
            AI-powered crop protection
          </div>

          <h2 className="max-w-2xl text-5xl font-extrabold leading-tight tracking-tight text-slate-900 md:text-6xl">
            Protect your crops with
            <span className="text-green-600"> smarter detection.</span>
          </h2>

          <p className="mt-6 max-w-xl text-lg leading-8 text-slate-600">
            Upload a clear image of your crop and get AI-powered disease
            detection with helpful insights for better crop care.
          </p>

          <div className="mt-8 flex flex-wrap gap-4">
            <a
              href="#detect"
              className="rounded-xl bg-green-600 px-6 py-3.5 font-semibold text-white shadow-lg shadow-green-200 transition hover:bg-green-700"
            >
              Detect Crop Disease →
            </a>

            <a
              href="#about"
              className="rounded-xl border border-slate-200 bg-white px-6 py-3.5 font-semibold text-slate-700 transition hover:border-green-200 hover:bg-green-50"
            >
              Learn More
            </a>
          </div>

          <div className="mt-10 flex flex-wrap gap-6 text-sm text-slate-600">
            <span>✓ Easy to use</span>
            <span>✓ Image based detection</span>
            <span>✓ Farmer friendly</span>
          </div>
        </div>

        {/* Hero visual */}
        <div className="relative">
          <div className="absolute -inset-6 rounded-[2rem] bg-green-100/70 blur-3xl" />

          <div className="relative overflow-hidden rounded-[2rem] border border-green-100 bg-white p-8 shadow-2xl shadow-green-100">
            <div className="rounded-2xl bg-gradient-to-br from-green-50 to-emerald-100 p-10 text-center">
              <div className="mx-auto flex h-32 w-32 items-center justify-center rounded-full bg-white text-7xl shadow-lg">
                🌾
              </div>

              <h3 className="mt-7 text-2xl font-bold text-green-900">
                Healthy crops start with early detection
              </h3>

              <p className="mt-3 text-sm leading-6 text-green-800/70">
                Upload your crop image to begin the analysis process.
              </p>
            </div>

            <div className="mt-6 grid grid-cols-3 gap-3 text-center">
              <div className="rounded-xl bg-slate-50 p-3">
                <div className="text-xl">📷</div>
                <p className="mt-1 text-xs font-medium text-slate-600">
                  Upload
                </p>
              </div>

              <div className="rounded-xl bg-slate-50 p-3">
                <div className="text-xl">🤖</div>
                <p className="mt-1 text-xs font-medium text-slate-600">
                  Analyze
                </p>
              </div>

              <div className="rounded-xl bg-slate-50 p-3">
                <div className="text-xl">💡</div>
                <p className="mt-1 text-xs font-medium text-slate-600">
                  Insights
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Upload section */}
      <section id="detect" className="bg-white px-6 py-20">
        <div className="mx-auto max-w-4xl">
          <div className="text-center">
            <span className="text-sm font-bold uppercase tracking-widest text-green-600">
              Disease Detection
            </span>

            <h2 className="mt-3 text-4xl font-extrabold tracking-tight text-slate-900">
              Upload your crop image
            </h2>

            <p className="mx-auto mt-4 max-w-2xl text-slate-600">
              Upload a clear image of the affected crop or leaf. Our system
              will use the image for disease analysis.
            </p>
          </div>

          <div className="mt-10">
            {!preview ? (
              <div
                onDragOver={(event) => {
                  event.preventDefault();
                  setIsDragging(true);
                }}
                onDragLeave={() => setIsDragging(false)}
                onDrop={handleDrop}
                onClick={() => fileInputRef.current?.click()}
                className={`cursor-pointer rounded-3xl border-2 border-dashed p-10 text-center transition md:p-16 ${
                  isDragging
                    ? "border-green-600 bg-green-50"
                    : "border-green-200 bg-green-50/40 hover:border-green-400 hover:bg-green-50"
                }`}
              >
                <input
                  ref={fileInputRef}
                  type="file"
                  accept="image/png,image/jpeg,image/jpg"
                  onChange={handleFileChange}
                  className="hidden"
                />

                <div className="mx-auto flex h-20 w-20 items-center justify-center rounded-2xl bg-white text-4xl shadow-md">
                  📷
                </div>

                <h3 className="mt-6 text-xl font-bold text-slate-900">
                  Drag & drop your crop image
                </h3>

                <p className="mt-2 text-slate-500">
                  or click anywhere here to choose an image
                </p>

                <button
                  type="button"
                  className="mt-6 rounded-xl bg-green-600 px-6 py-3 font-semibold text-white transition hover:bg-green-700"
                >
                  Choose Image
                </button>

                <p className="mt-5 text-xs text-slate-400">
                  JPG, JPEG or PNG • Maximum size 10 MB
                </p>
              </div>
            ) : (
              <div className="rounded-3xl border border-green-100 bg-green-50/50 p-6 md:p-8">
                <div className="grid gap-8 md:grid-cols-2">
                  <div className="overflow-hidden rounded-2xl bg-slate-100">
                    <img
                      src={preview}
                      alt="Selected crop"
                      className="h-80 w-full object-cover"
                    />
                  </div>

                  <div className="flex flex-col justify-center">
                    <span className="text-sm font-semibold text-green-600">
                      IMAGE READY
                    </span>

                    <h3 className="mt-2 break-all text-2xl font-bold text-slate-900">
                      {selectedImage?.name}
                    </h3>

                    <p className="mt-2 text-sm text-slate-500">
                      {selectedImage
                        ? `${(selectedImage.size / 1024 / 1024).toFixed(2)} MB`
                        : ""}
                    </p>

                    <div className="mt-6 flex flex-col gap-3 sm:flex-row">
                      <button
                        onClick={() => fileInputRef.current?.click()}
                        className="rounded-xl border border-green-200 bg-white px-5 py-3 font-semibold text-green-700 hover:bg-green-50"
                      >
                        Change Image
                      </button>

                      <button
                        onClick={() => {
                          alert(
                            "Image is ready. Backend API integration will be added in the next integration sprint."
                          );
                        }}
                        className="rounded-xl bg-green-600 px-5 py-3 font-semibold text-white hover:bg-green-700"
                      >
                        Analyze Crop →
                      </button>
                    </div>

                    <button
                      onClick={removeImage}
                      className="mt-4 text-left text-sm font-medium text-red-500 hover:text-red-600"
                    >
                      Remove image
                    </button>
                  </div>
                </div>
              </div>
            )}

            {error && (
              <div className="mt-4 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm font-medium text-red-600">
                ⚠ {error}
              </div>
            )}
          </div>
        </div>
      </section>

      {/* About */}
      <section id="about" className="bg-[#f7faf5] px-6 py-20">
        <div className="mx-auto max-w-7xl">
          <div className="grid gap-8 md:grid-cols-3">
            <div className="rounded-2xl bg-white p-7 shadow-sm">
              <div className="text-3xl">📸</div>
              <h3 className="mt-5 text-xl font-bold">Simple Upload</h3>
              <p className="mt-2 text-sm leading-6 text-slate-600">
                Farmers can easily upload crop images through a responsive
                interface.
              </p>
            </div>

            <div className="rounded-2xl bg-white p-7 shadow-sm">
              <div className="text-3xl">🤖</div>
              <h3 className="mt-5 text-xl font-bold">AI Detection</h3>
              <p className="mt-2 text-sm leading-6 text-slate-600">
                Uploaded images can later be sent to the project's AI model
                for disease detection.
              </p>
            </div>

            <div className="rounded-2xl bg-white p-7 shadow-sm">
              <div className="text-3xl">🌱</div>
              <h3 className="mt-5 text-xl font-bold">Crop Care</h3>
              <p className="mt-2 text-sm leading-6 text-slate-600">
                The platform is designed to help farmers make better crop-care
                decisions.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-green-100 bg-white px-6 py-8">
        <div className="mx-auto flex max-w-7xl flex-col items-center justify-between gap-3 text-sm text-slate-500 md:flex-row">
          <p>© 2026 Crop Care Crop. Academic Project.</p>
          <p>AI-powered crop disease detection</p>
        </div>
      </footer>
    </main>
  );
}