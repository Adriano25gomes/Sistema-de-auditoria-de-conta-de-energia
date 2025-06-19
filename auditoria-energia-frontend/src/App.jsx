import { useState } from 'react'
import { Upload, FileText, History, AlertTriangle, CheckCircle } from 'lucide-react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Alert, AlertDescription } from '@/components/ui/alert.jsx'
import './App.css'

function App() {
  const [selectedFile, setSelectedFile] = useState(null)
  const [isUploading, setIsUploading] = useState(false)
  const [auditResult, setAuditResult] = useState(null)
  const [error, setError] = useState(null)

  const handleFileSelect = (event) => {
    const file = event.target.files[0]
    if (file) {
      setSelectedFile(file)
      setError(null)
      setAuditResult(null)
    }
  }

  const handleUpload = async () => {
    if (!selectedFile) {
      setError('Por favor, selecione um arquivo')
      return
    }

    setIsUploading(true)
    setError(null)

    const formData = new FormData()
    formData.append('file', selectedFile)

    try {
      const response = await fetch('http://localhost:5000/api/upload', {
        method: 'POST',
        body: formData,
      })

      const data = await response.json()

      if (response.ok) {
        setAuditResult(data.resultado)
        setSelectedFile(null)
        // Limpar o input file
        document.getElementById('file-input').value = ''
      } else {
        setError(data.error || 'Erro ao processar arquivo')
      }
    } catch (err) {
      setError('Erro de conexão com o servidor')
    } finally {
      setIsUploading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 p-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Sistema de Auditoria de Contas de Energia Elétrica
          </h1>
          <p className="text-gray-600">
            Governo do Estado de Rondônia - Ferramenta automatizada para auditoria de faturas
          </p>
        </div>

        {/* Upload Section */}
        <Card className="mb-6">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Upload className="h-5 w-5" />
              Upload de Conta de Energia
            </CardTitle>
            <CardDescription>
              Faça o upload da conta de energia em formato PDF ou imagem (PNG, JPG)
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div>
                <input
                  id="file-input"
                  type="file"
                  accept=".pdf,.png,.jpg,.jpeg"
                  onChange={handleFileSelect}
                  className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
                />
              </div>
              
              {selectedFile && (
                <div className="flex items-center gap-2 text-sm text-gray-600">
                  <FileText className="h-4 w-4" />
                  {selectedFile.name} ({(selectedFile.size / 1024 / 1024).toFixed(2)} MB)
                </div>
              )}

              <Button 
                onClick={handleUpload} 
                disabled={!selectedFile || isUploading}
                className="w-full"
              >
                {isUploading ? 'Processando...' : 'Iniciar Auditoria'}
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Error Alert */}
        {error && (
          <Alert className="mb-6 border-red-200 bg-red-50">
            <AlertTriangle className="h-4 w-4 text-red-600" />
            <AlertDescription className="text-red-800">
              {error}
            </AlertDescription>
          </Alert>
        )}

        {/* Results Section */}
        {auditResult && (
          <Card className="mb-6">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <CheckCircle className="h-5 w-5 text-green-600" />
                Resultado da Auditoria
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="bg-green-50 p-4 rounded-lg">
                    <div className="text-sm text-green-600 font-medium">Status</div>
                    <div className="text-lg font-semibold text-green-800">
                      {auditResult.resumo?.status_geral || 'Processado'}
                    </div>
                  </div>
                  <div className="bg-blue-50 p-4 rounded-lg">
                    <div className="text-sm text-blue-600 font-medium">Irregularidades</div>
                    <div className="text-lg font-semibold text-blue-800">
                      {auditResult.resumo?.total_irregularidades || 0}
                    </div>
                  </div>
                  <div className="bg-orange-50 p-4 rounded-lg">
                    <div className="text-sm text-orange-600 font-medium">Impacto Financeiro</div>
                    <div className="text-lg font-semibold text-orange-800">
                      R$ {auditResult.resumo?.impacto_financeiro?.toFixed(2) || '0,00'}
                    </div>
                  </div>
                </div>
                
                <div className="text-sm text-gray-600">
                  <strong>Arquivo processado:</strong> {auditResult.arquivo}
                </div>
                <div className="text-sm text-gray-600">
                  <strong>Data do processamento:</strong> {new Date(auditResult.data_processamento).toLocaleString('pt-BR')}
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        {/* History Section */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <History className="h-5 w-5" />
              Histórico de Auditorias
            </CardTitle>
            <CardDescription>
              Últimas auditorias realizadas
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="text-center text-gray-500 py-8">
              Nenhuma auditoria anterior encontrada
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

export default App

