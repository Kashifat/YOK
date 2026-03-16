"use client"

import { useState } from "react"
import { ChevronDown, ChevronUp, X } from "lucide-react"

interface FilterOption {
  label: string
  value: string
  count?: number
}

interface FilterSection {
  title: string
  options: FilterOption[]
}

const filterSections: FilterSection[] = [
  {
    title: "Catégorie",
    options: [
      { label: "Robes", value: "robes", count: 1245 },
      { label: "Tops & Blouses", value: "tops", count: 892 },
      { label: "Pantalons", value: "pantalons", count: 654 },
      { label: "Jeans", value: "jeans", count: 421 },
      { label: "Jupes", value: "jupes", count: 312 },
      { label: "Vestes", value: "vestes", count: 278 },
    ],
  },
  {
    title: "Taille",
    options: [
      { label: "XS", value: "xs" },
      { label: "S", value: "s" },
      { label: "M", value: "m" },
      { label: "L", value: "l" },
      { label: "XL", value: "xl" },
      { label: "XXL", value: "xxl" },
    ],
  },
  {
    title: "Couleur",
    options: [
      { label: "Noir", value: "#000000" },
      { label: "Blanc", value: "#FFFFFF" },
      { label: "Rouge", value: "#EF4444" },
      { label: "Bleu", value: "#3B82F6" },
      { label: "Rose", value: "#EC4899" },
      { label: "Vert", value: "#22C55E" },
      { label: "Beige", value: "#D4B896" },
      { label: "Gris", value: "#9CA3AF" },
    ],
  },
  {
    title: "Prix",
    options: [
      { label: "Moins de 10$", value: "0-10" },
      { label: "10$ - 20$", value: "10-20" },
      { label: "20$ - 30$", value: "20-30" },
      { label: "30$ - 50$", value: "30-50" },
      { label: "Plus de 50$", value: "50+" },
    ],
  },
  {
    title: "Style",
    options: [
      { label: "Casual", value: "casual" },
      { label: "Élégant", value: "elegant" },
      { label: "Bohème", value: "boheme" },
      { label: "Streetwear", value: "streetwear" },
      { label: "Vintage", value: "vintage" },
      { label: "Minimaliste", value: "minimaliste" },
    ],
  },
]

interface ProductFiltersProps {
  onFilterChange?: (filters: Record<string, string[]>) => void
  isMobile?: boolean
  onClose?: () => void
}

export function ProductFilters({ onFilterChange, isMobile, onClose }: ProductFiltersProps) {
  const [openSections, setOpenSections] = useState<string[]>(["Catégorie", "Taille", "Prix"])
  const [selectedFilters, setSelectedFilters] = useState<Record<string, string[]>>({})

  const toggleSection = (title: string) => {
    setOpenSections((prev) =>
      prev.includes(title) ? prev.filter((t) => t !== title) : [...prev, title]
    )
  }

  const toggleFilter = (section: string, value: string) => {
    setSelectedFilters((prev) => {
      const current = prev[section] || []
      const updated = current.includes(value)
        ? current.filter((v) => v !== value)
        : [...current, value]
      const newFilters = { ...prev, [section]: updated }
      onFilterChange?.(newFilters)
      return newFilters
    })
  }

  const clearAllFilters = () => {
    setSelectedFilters({})
    onFilterChange?.({})
  }

  const totalFilters = Object.values(selectedFilters).flat().length

  return (
    <aside className={`${isMobile ? "p-4" : ""}`}>
      {/* Header */}
      <div className="flex items-center justify-between mb-4 pb-4 border-b border-border">
        <h2 className="font-semibold text-lg">Filtres</h2>
        <div className="flex items-center gap-2">
          {totalFilters > 0 && (
            <button
              onClick={clearAllFilters}
              className="text-sm text-muted-foreground hover:text-foreground transition-colors"
            >
              Tout effacer ({totalFilters})
            </button>
          )}
          {isMobile && onClose && (
            <button onClick={onClose} className="p-1">
              <X className="h-5 w-5" />
            </button>
          )}
        </div>
      </div>

      {/* Filter Sections */}
      <div className="space-y-4">
        {filterSections.map((section) => (
          <div key={section.title} className="border-b border-border pb-4">
            <button
              onClick={() => toggleSection(section.title)}
              className="flex items-center justify-between w-full py-2 font-medium text-sm"
            >
              {section.title}
              {openSections.includes(section.title) ? (
                <ChevronUp className="h-4 w-4" />
              ) : (
                <ChevronDown className="h-4 w-4" />
              )}
            </button>
            {openSections.includes(section.title) && (
              <div className="mt-2 space-y-2">
                {section.title === "Couleur" ? (
                  <div className="flex flex-wrap gap-2">
                    {section.options.map((option) => (
                      <button
                        key={option.value}
                        onClick={() => toggleFilter(section.title, option.value)}
                        className={`w-7 h-7 rounded-full border-2 transition-all ${
                          selectedFilters[section.title]?.includes(option.value)
                            ? "border-foreground scale-110"
                            : "border-border hover:border-muted-foreground"
                        }`}
                        style={{ backgroundColor: option.value }}
                        title={option.label}
                      />
                    ))}
                  </div>
                ) : section.title === "Taille" ? (
                  <div className="flex flex-wrap gap-2">
                    {section.options.map((option) => (
                      <button
                        key={option.value}
                        onClick={() => toggleFilter(section.title, option.value)}
                        className={`px-3 py-1.5 text-sm border rounded transition-colors ${
                          selectedFilters[section.title]?.includes(option.value)
                            ? "bg-foreground text-background border-foreground"
                            : "border-border hover:border-foreground"
                        }`}
                      >
                        {option.label}
                      </button>
                    ))}
                  </div>
                ) : (
                  <div className="space-y-1">
                    {section.options.map((option) => (
                      <label
                        key={option.value}
                        className="flex items-center gap-2 py-1 cursor-pointer group"
                      >
                        <input
                          type="checkbox"
                          checked={selectedFilters[section.title]?.includes(option.value) || false}
                          onChange={() => toggleFilter(section.title, option.value)}
                          className="w-4 h-4 rounded border-border accent-foreground"
                        />
                        <span className="text-sm group-hover:text-foreground transition-colors">
                          {option.label}
                        </span>
                        {option.count && (
                          <span className="text-xs text-muted-foreground ml-auto">
                            ({option.count})
                          </span>
                        )}
                      </label>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Apply Button - Mobile */}
      {isMobile && (
        <div className="mt-6">
          <button
            onClick={onClose}
            className="w-full py-3 bg-foreground text-background font-medium rounded hover:opacity-90 transition-opacity"
          >
            Appliquer les filtres {totalFilters > 0 && `(${totalFilters})`}
          </button>
        </div>
      )}
    </aside>
  )
}
