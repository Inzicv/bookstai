import { HitlStepCard } from '@/components/HitlStepCard'

export function ImageStoryboardSceneCard({ scene, onApprove, onReject, onEdit }: any) {
  return (
    <HitlStepCard
      step={{
        name: scene.scene_id,
        status: scene.status ?? 'pending',
        content: scene,
      }}
      onApprove={onApprove}
      onReject={onReject}
      onEdit={onEdit}
    />
  )
}
