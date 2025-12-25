import {
  Heading,
  Text,
  Button,
  Avatar,
  RevealFx,
  Column,
  Badge,
  Row,
  Schema,
  Meta,
  Line,
} from "@once-ui-system/core";
import { home, about, person, baseURL, routes } from "@/resources";
import { Mailchimp } from "@/components";
import { Projects } from "@/components/work/Projects";
import { Posts } from "@/components/blog/Posts";

export async function generateMetadata() {
  return Meta.generate({
    title: home.title,
    description: home.description,
    baseURL: baseURL,
    path: home.path,
    image: home.image,
  });
}

export default function Home() {
  return (
    <Column maxWidth="m" gap="xl" paddingY="12" horizontal="center">
      {/* ========================================
          SEO STRUCTURED DATA (Schema.org)
          Generates webPage schema for search engines
          Author image: /images/xia.jpg
      ======================================== */}
      <Schema
        as="webPage"
        baseURL={baseURL}
        path={home.path}
        title={home.title}
        description={home.description}
        image={`/api/og/generate?title=${encodeURIComponent(home.title)}`}
        author={{
          name: person.name,
          url: `${baseURL}${about.path}`,
          image: `${baseURL}${person.avatar}`,
        }}
      />

      {/* ========================================
          HERO SECTION
          - Featured badge: "Ignite 2025 - Featured work"
          - Headline: "Learning at the Intersection of Data and Software"
          - Subline: Introduction text (NUS student, full-stack & data science)
          - CTA Button: Links to /about with avatar (/images/xia.jpg)
      ======================================== */}
      <Column fillWidth horizontal="center" gap="m">
        <Column maxWidth="s" horizontal="center" align="center">
          {home.featured.display && (
            <RevealFx
              fillWidth
              horizontal="center"
              paddingTop="16"
              paddingBottom="32"
              paddingLeft="12"
            >
              <Badge
                background="brand-alpha-weak"
                paddingX="12"
                paddingY="4"
                onBackground="neutral-strong"
                textVariant="label-default-s"
                arrow={false}
                href={home.featured.href}
              >
                <Row paddingY="2">{home.featured.title}</Row>
              </Badge>
            </RevealFx>
          )}
          <RevealFx translateY="4" fillWidth horizontal="center" paddingBottom="16">
            <Heading wrap="balance" variant="display-strong-l">
              {home.headline}
            </Heading>
          </RevealFx>
          <RevealFx translateY="8" delay={0.2} fillWidth horizontal="center" paddingBottom="32">
            <Text wrap="balance" onBackground="neutral-weak" variant="heading-default-xl">
              {home.subline}
            </Text>
          </RevealFx>
          <RevealFx paddingTop="12" delay={0.4} horizontal="center" paddingLeft="12">
            <Button
              id="about"
              data-border="rounded"
              href={about.path}
              variant="secondary"
              size="m"
              weight="default"
              arrowIcon
            >
              <Row gap="8" vertical="center" paddingRight="4">
                {about.avatar.display && (
                  <Avatar
                    marginRight="8"
                    style={{ marginLeft: "-0.75rem" }}
                    src={person.avatar}
                    size="m"
                  />
                )}
                {about.title}
              </Row>
            </Button>
          </RevealFx>
        </Column>
      </Column>

      {/* ========================================
          FEATURED PROJECT (1st Project)
          Project: "Ignite 2025: Building with Agentic AI"
          File: src/app/work/projects/ignite-2025-building-with-agentic-ai.mdx
          Cover image: /images/projects/agentic-ai-ignite/github-repo-screenshot.jpg
      ======================================== */}
      <RevealFx translateY="16" delay={0.6}>
        <Projects range={[2, 2]} />
      </RevealFx>

      {/* ========================================
          LATEST BLOG POSTS SECTION
          Displays 2 most recent blog posts:
          - Post 1: "Create, edit and delete blog posts" (2025-03-17)
            File: src/app/blog/posts/blog.mdx
          - Post 2: "Using custom components in markdown" (2025-04-20)
            File: src/app/blog/posts/components.mdx
          Layout: 2-column grid with decorative lines (top/bottom)
      ======================================== */}
      {routes["/blog"] && (
        <Column fillWidth gap="24" marginBottom="l">
          <Row fillWidth paddingRight="64">
            <Line maxWidth={48} />
          </Row>
          <Row fillWidth gap="24" marginTop="40" s={{ direction: "column" }}>
            <Row flex={1} paddingLeft="l" paddingTop="24">
              <Heading as="h2" variant="display-strong-xs" wrap="balance">
                Latest from the blog
              </Heading>
            </Row>
            <Row flex={3} paddingX="20">
              <Posts range={[1, 2]} columns="2" />
            </Row>
          </Row>
          <Row fillWidth paddingLeft="64" horizontal="end">
            <Line maxWidth={48} />
          </Row>
        </Column>
      )}

      {/* ========================================
          REMAINING PROJECTS GRID (Projects 2 & 3)
          - Project 2: "Automating Design Handovers with a Figma to Code Pipeline"
            File: src/app/work/projects/automate-design-handovers-with-a-figma-to-code-pipeline.mdx
            Images: /images/projects/project-01/cover-02.jpg, image-03.jpg
          - Project 3: "Once UI: Open-source design system"
            File: src/app/work/projects/simple-portfolio-builder.mdx
            Images: /images/projects/project-01/cover-04.jpg, video-01.mp4
      ======================================== */}
      <Projects range={[1, 1]} />
      <Projects range={[3]} />

      {/* ========================================
          NEWSLETTER SIGNUP SECTION
          Title: "Subscribe to Tangzihan's Newsletter"
          Description: "My weekly newsletter about creativity and engineering"
          Uses Mailchimp form component
      ======================================== */}
      <Mailchimp /> 
    </Column>
  );
}
